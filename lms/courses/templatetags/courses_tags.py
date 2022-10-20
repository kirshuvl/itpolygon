from django import template
from django.utils.safestring import mark_safe
from lms.lessons.models import Lesson
from lms.steps.models import QuestionStep, Step, UserAnswerForQuestionStep
register = template.Library()


@register.simple_tag
def step_color(step, user):
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
def get_steps(steps, user):
    string = ''
    for step in steps:
        string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded opacity-50"><i class="bi {}"></i></span></a> '.\
            format(step.get_absolute_url(), step_color(
                step, user), step.step_icon_class())
    return mark_safe(string)


@register.simple_tag
def get_steps_in_step(steps, user, cur_step):
    string = ''
    for step in steps:
        if step == cur_step:
            string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded"><i class="bi {}"></i></span></a> '.\
                format(step.get_absolute_url(), step_color(
                    step, user), step.step_icon_class())
        else:
            string += '<a href="{}" class="text-decoration-none"><span class="badge bg-{} p-2 rounded opacity-50"><i class="bi {}"></i></span></a> '.\
                format(step.get_absolute_url(), step_color(
                    step, user), step.step_icon_class())
    return mark_safe(string)


@register.simple_tag
def lesson_next_step(lesson, steps, user):
    if lesson.type == 'ST':
        text = 'Начать урок'
    elif lesson.type == 'QZ':
        text = 'Начать тест'
    return mark_safe(button(steps.first().get_absolute_url(), 'secondary', text))


@register.simple_tag
def previous_step(current_step, steps):
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
        previous = steps[position - 1].get_absolute_url()
        if current_step.lesson.type == 'ST':
            text = 'Предыдущий шаг'
        elif current_step.lesson.type == 'QZ':
            text = 'Предыдущий вопрос'
    button = '<div class="col"><a href="{}" class="btn btn-outline-secondary shadow col-12">{}</a></div>'.format(
        previous, text)
    return mark_safe(button)


@register.simple_tag
def next_step(current_step, steps, user, attempts):
    if current_step.lesson.type == 'ST':
        return next_step_for_standart_lesson(current_step, steps, user, attempts)
    elif current_step.lesson.type == 'QZ':
        return next_step_for_quiz_lesson(current_step, steps, user)


def next_step_for_standart_lesson(current_step, steps, user, attempts):
    position, enroll = get_position_and_enroll(current_step, steps, user)
    color = 'secondary'
    if enroll.status == 'PR':
        if current_step.type() == 'text' or current_step.type() == 'video':
            return button(current_step.end_step(), 'success', 'Материал изучен!')
        else:
            return button('', 'danger', 'Нужно ответить на вопрос правильно или исчерпать попытки')
    elif enroll.status == 'RP':
        return button(current_step.end_step(), 'success', 'Материал повторен!')
    elif enroll.status == 'WA':
        if current_step.num_attempts == len(attempts):
            return last_or_not_steps(current_step, steps, position)
        return button('', 'danger', 'Оставшееся количество попыток: {}'.format(current_step.num_attempts - len(attempts)))

    return last_or_not_steps(current_step, steps, position)


def last_or_not_steps(current_step, steps, position):
    if position == len(steps) - 1:
        next = current_step.lesson.get_absolute_url()
        text = 'Закончить урок'
    else:
        next = steps[position + 1].get_absolute_url()
        text = 'Следующий шаг'

    return mark_safe(button(next, 'secondary', text))


def last_or_not_question(current_step, steps, position):
    if position == len(steps) - 1:
        next = current_step.lesson.get_absolute_url()
        text = 'Закончить тест'
    else:
        next = steps[position + 1].get_absolute_url()
        text = 'Следующий вопрос'

    return mark_safe(button(next, 'secondary', text))


def next_step_for_quiz_lesson(current_step, steps, user):
    position, enroll = get_position_and_enroll(current_step, steps, user)
    return last_or_not_question(current_step, steps, position)


def button(next, color, text):
    return mark_safe('<div class="col"><a href="{}" class="btn btn-outline-{} shadow col-12">{}</a></div>'.
                     format(next, color, text)
                     )


def get_position_and_enroll(current_step, steps, user):
    for position, step in enumerate(steps):
        if current_step == step:
            break
    for enroll in current_step.steps_enrolls.all():
        if enroll.user == user:
            break
    return position, enroll


@register.filter
def user_has_right_answer(user, attempts):
    for attempt in attempts:
        if attempt.is_correct:
            return True
    return False


@register.simple_tag
def topic_get_color(topic, user):
    for enroll in topic.topics_enrolls.all():
        if enroll.user == user:
            if enroll.status == 'OK':
                return 'success'
            if enroll.status == 'PR':
                return 'primary'
            elif enroll.status == 'RP':
                return 'warning'
    return 'secondary'


@register.simple_tag
def lesson_get_color(lesson, user):
    for enroll in lesson.lessons_enrolls.all():
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
def is_user_end_lesson(lesson, steps, user):
    for enroll in lesson.lessons_enrolls.all():
        if enroll.user == user:
            if enroll.status == 'OK':
                return mark_safe('')
    ok = True
    for step in steps:
        for enroll in step.steps_enrolls.all():
            if enroll.user == user and enroll.status != 'OK':
                ok = False
                break
        else:
            return mark_safe('')
    if ok:
        return button(lesson.end_lesson(), 'success', 'Закончить урок!')
    return button('', 'secondary', 'Есть ошибки или непройденные шаги')


@register.filter
def point(time):
    return str(time).replace(',', '.')