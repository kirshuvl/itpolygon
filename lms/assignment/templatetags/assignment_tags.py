from django import template
register = template.Library()


@register.simple_tag
def get_file_name(file_name):
    return file_name.split('/')[-1].split('.')[0]


@register.simple_tag
def get_file_format(file_name):
    return file_name.split('/')[-1].split('.')[-1]
