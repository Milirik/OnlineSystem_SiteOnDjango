# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import StudentCodeModel
#
#
# @receiver(post_save, sender=StudentCodeModel)
# def my_handler(sender, **kwargs):
#     print('hi')
#     path = f'documents/answers/{sender.student.username}_{"_".join(sender.task.title.split())}/file.txt'
#     with open(path, 'w') as f:
#         f.write(sender.code_text)
