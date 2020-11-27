import json
import threading
import pika
from testing_system.models import StudentCodeModel, Task, Student


class AMQPConsuming(threading.Thread):
    flag = False

    def callback(self, ch, method, properties, body):
        print(body)
        # Проверка на пустое сообщение
        if body:
            ans = body.decode('utf-8')
            ans_s = json.loads(ans)
            st_ans = StudentCodeModel.objects.filter(pk=ans_s["answer_id"]).first()
            if st_ans:
                st_ans.status = ans_s["status"]
                st_ans.save()
                # print(st_ans.status)
            else:
                pass
                # Не нашел запись
        else:
            print("Пришел пустой ответ")


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
