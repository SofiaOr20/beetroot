from django.template import Library
import datetime
register = Library()

@register.filter
def date_format(value):
    return datetime.datetime.strftime(value, '%d-%m-%y %H:%m')
