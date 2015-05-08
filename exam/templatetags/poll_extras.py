__author__ = 'Alexey Kutepov'

from django import template

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def to_class_name(value):
    return value.__class__.__name__