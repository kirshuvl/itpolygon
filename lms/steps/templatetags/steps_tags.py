from django.utils.safestring import mark_safe
from django import template
register = template.Library()


@register.simple_tag
def step_get_steps(steps, current_step):
    string = ''
    for step in steps:
        if step == current_step:
            string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded"><i class="bi {}"></i></span></a> '.\
                format(step.get_absolute_url(), step_color(
                    step), step.step_icon_class())
        else:
            string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded opacity-50"><i class="bi {}"></i></span></a> '.\
                format(step.get_absolute_url(), step_color(
                    step), step.step_icon_class())
    return mark_safe(string)


@register.simple_tag
def previous_step(steps, current_step):

    for position, step in enumerate(steps):
        if current_step == step:
            break
    if position == 0:
        previous = current_step.lesson.get_absolute_url()
        if current_step.lesson.type == 'ST':
            text = 'Вернуться к описанию урока'
        elif current_step.lesson.type == 'QZ':
            text = 'Вернуться к описанию теста'
        else:
            text = 'Вернуться к описанию контеста'
    else:
        previous = steps[position - 1].get_absolute_url()
        if current_step.lesson.type == 'ST':
            text = 'Предыдущий шаг'
        elif current_step.lesson.type == 'QZ':
            text = 'Предыдущий вопрос'
        else:
            text = 'Следующая задача'
    button = '<div class="col"><a href="{}" class="btn btn-outline-secondary shadow col-12">{}</a></div>'.format(
        previous, text)
    return mark_safe(button)


@register.simple_tag
def user_end_step(current_step):
    enroll = current_step.steps_enrolls.first()
    if current_step.type() == 'text' or current_step.type() == 'video':
        if enroll is None or enroll.status == 'PR':
            return button(current_step.end_step(), 'success', 'Материал изучен!')
        elif enroll.status == 'RP':
            return button(current_step.end_step(), 'success', 'Материал повторен!')
    return mark_safe('')


@register.simple_tag
def next_step(steps, current_step, attempts):
    if current_step.lesson.type == 'ST':
        return next_step_for_standart_lesson(steps, current_step, attempts)
    elif current_step.lesson.type == 'QZ':
        return next_step_for_quiz_lesson(steps, current_step, attempts)


def next_step_for_standart_lesson(steps, current_step, attempts):
    enroll = current_step.steps_enrolls.first()
    if enroll is None or enroll.status == 'PR':
        if current_step.type() == 'text' or current_step.type() == 'video':
            return button(current_step.end_step(), 'success', 'Материал изучен!')
        else:
            return button('', 'danger', 'Нужно ответить на вопрос правильно или исчерпать попытки')
    elif enroll.status == 'RP':
        return button(current_step.end_step(), 'success', 'Материал повторен!')
    elif enroll.status == 'WA':
        if current_step.num_attempts == len(attempts):
            return last_or_not_steps(steps, current_step)
        return button('', 'danger', 'Оставшееся количество попыток: {}'.format(current_step.num_attempts - len(attempts)))

    return last_or_not_steps(steps, current_step)


def last_or_not_steps(steps, current_step):
    position = get_step_position(steps, current_step)
    if position == len(steps) - 1:
        next = current_step.lesson.get_absolute_url()
        text = 'Закончить урок'
    else:
        next = steps[position + 1].get_absolute_url()
        text = 'Следующий шаг'

    return mark_safe(button(next, 'secondary', text))


def last_or_not_question(steps, current_step):
    position = get_step_position(steps, current_step)
    if position == len(steps) - 1:
        next = current_step.lesson.get_absolute_url()
        text = 'Закончить тест'
    else:
        next = steps[position + 1].get_absolute_url()
        text = 'Следующий вопрос'

    return mark_safe(button(next, 'secondary', text))


def next_step_for_quiz_lesson(current_step, steps, user):
    position, enroll = get_step_position(current_step, steps, user)
    return last_or_not_question(current_step, steps, position)


def get_step_position(steps, current_step):
    for position, step in enumerate(steps):
        if current_step == step:
            break
    return position

@register.filter
def step_color(step):
    enroll = step.steps_enrolls.first()
    if enroll is None:
        return 'secondary'
    if enroll.status == 'OK':
        return 'success'
    if enroll.status == 'PR':
        return 'primary'
    elif enroll.status == 'RP':
        return 'warning'
    elif enroll.status == 'WA':
        return 'danger'
    return 'secondary'


def button(next, color, text):
    return mark_safe('<div class="col"><a href="{}" class="btn btn-{} shadow col-12">{}</a></div>'.
                     format(next, color, text)
                     )
