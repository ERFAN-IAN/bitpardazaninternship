import jdatetime
from django import template

register = template.Library()


@register.filter
def to_jalali(value):
    if value:
        return jdatetime.date.fromgregorian(date=value).strftime('%Y/%m/%d')
    return value
