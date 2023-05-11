from django import template
from django.utils.safestring import mark_safe
from lms.steps.templatetags.steps_tags import button, step_color
from lms.steps.models import *
register = template.Library()


@register.simple_tag
def lesson_get_steps(lesson):
    string = ''
    for step in lesson.steps.all():
        string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded opacity-50"><i class="bi {}"></i></span></a> '.\
            format(step.get_absolute_url, step_color(
                step), step.step_icon_class)
    return mark_safe(string)


@register.simple_tag
def lesson_next_step(lesson):
    first_step = lesson.steps.first()

    if not first_step:
        return button('', 'secondary', 'Пока что урок пустой')
    else:
        text = 'Начать'
    return mark_safe(button(first_step.get_absolute_url, 'secondary', text))


@register.simple_tag
def step_colors(step, user):
    for enroll in step.steps_enrolls.all():
        if enroll.user == user:
            if enroll.status == 'OK':
                return 'success'
            if enroll.status == 'PR':
                return 'primary'
            elif enroll.status == 'RP':
                return 'warning'
            elif enroll.status == 'WA':
                return 'danger'
    return 'secondary'


@register.simple_tag
def date_counter(enrolls, day):
    
    for enroll in enrolls:
        if enroll.grouper == day:
            return len(enroll.list)

    return 0


@register.simple_tag
def col_bootstrap(counter, parent):

    
    if counter == 9 or counter == 8:
        return ''
    
    if counter == 7:
        return 'd-none d-sm-block'

    if counter == 6 or (counter == 5 and (parent == 3 or parent == 4)):
        return 'd-none d-md-block'
    
    if (counter == 5 and (parent == 1 or parent == 2)) or (counter == 4) or (counter == 3 and (parent == 3 or parent == 4)):
        return 'd-none d-lg-block'

    if counter == 2 or (counter == 3 and (parent == 1 or parent == 2)):
        return 'd-none d-xl-block' 
    
    if counter == 1:
        return 'd-none d-xxl-block'


    return ''


@register.simple_tag
def foo(qwerty):

    #print(type(qwerty.type()))

    if str(qwerty.type()) == "<class 'lms.steps.models.TextStep'>":
        return 'text'
    
    return qwerty.type()