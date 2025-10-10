from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(format_string='%m %d %Y H:i'):
   return datetime.utcnow().strftime(format_string)