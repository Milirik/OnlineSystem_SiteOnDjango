from django import template

register = template.Library()


@register.filter(name='cut')
def cut(value):
    return str(value).split('/')[-1]


@register.filter(name='number_cut')
def number_cut(value):
    return str(round(value/1000, 1)) + " секунд"


@register.filter(name='number_cut2')
def number_cut2(value):
    value = str(value/1024) + " гигабайт" if value//1024 >0 else str(value) + " МБ"
    return value


@register.filter(name='cut_time')
def cut_time(value):
    tmp = str(value).split(':')
    tmp2 = tmp[2][0:1]
    return ':'.join([tmp[0], tmp[1], tmp2])

