from django import template

register = template.Library()


@register.filter(name='cut')
def cut(value):
    return str(value).split('/')[-1]


@register.filter(name='number_cut')
def number_cut(value):
    return str(round(value/1000/60, 1)) + " минут"


@register.filter(name='number_cut2')
def number_cut2(value):
    return str(round(value/1024, 5)) + " кбайт"
    return value