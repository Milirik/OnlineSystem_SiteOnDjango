import time


def user_directory_path(instance, filename):
    """Создает путь к папке ответа ученика"""
    # Костыль с определением типа файла
    return f'answers/{instance.student.username}_{"_".join(instance.task.title.split())}/{int(round(time.time()*1000))}' \
           f'/{filename}'


def course_image_path(instanse, filename):
    return f'images/courses/{instanse.title}_{filename}'