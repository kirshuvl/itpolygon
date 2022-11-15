from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def homework_steps_count(homework):
    cnt = homework.steps.count()
    return cnt