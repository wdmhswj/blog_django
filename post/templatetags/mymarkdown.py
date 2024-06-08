#coding=utf-8

from django.template import Library
from markdown import markdown
register = Library()

@register.filter
def md(value):
    return markdown(value)
