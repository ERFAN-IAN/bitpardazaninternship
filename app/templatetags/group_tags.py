import jdatetime
from django import template

register = template.Library()


# @register.filter
# def to_jalali(value):
#     if value:
#         return jdatetime.date.fromgregorian(date=value).strftime('%Y/%m/%d')
#     return value


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
