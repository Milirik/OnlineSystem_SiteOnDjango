import json
import threading
import pika
from testing_system.models import StudentCodeModel, Task, Student


class AMQPConsuming(threading.Thread):
    flag = False

    def callback(self, ch, method, properties, body):
        ans = body.decode('utf-8')
        ans_s = json.loads(ans)
        # print(ans_s["Errors"])
        # print(ans_s["Resources"])
        # print(ans_s["TestErrors"])

        st_ans = StudentCodeModel.objects.get(pk=ans_s["answer_id"])
        if st_ans:
            if ans_s["TestErrors"]:
                st_ans.status = f"Ошибка тестирования. Входные данные: {(ans_s['TestErrors'])['input']}, " \
                                f"Ожидаемый результат: {(ans_s['TestErrors'])['output']}"
            elif ans_s["Errors"]:
                st_ans.status = f"В процессе работы программы были выявлены следующие ошибки: {ans_s['Errors']}"
            else:
                st_ans.status = f"OK (Время работы: {ans_s['Resources']['time']}, Память: {ans_s['Resources']['memory']})"
            st_ans.save()
            print(st_ans.status)

    @staticmethod
    def _get_connection():
        return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='server_answers')
        print('[!] RABBITMQ RECEIVER RUN')
        channel.basic_consume(queue='server_answers', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()
