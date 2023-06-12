from django import template
from django.utils.safestring import mark_safe
register = template.Library()

'''


# Новое и используемое

@register.filter
def steps_finished(lesson):
    cnt = 0
    for step in lesson.steps.all():
        for enroll in step.steps_enrolls.all():
            if enroll is not None and enroll.status == 'OK':
                cnt += 1

    return cnt


@register.filter
def steps_counter(lesson):

    return lesson.steps.count()


@register.filter
def topic_progress(topic):
    cnt = 0
    for lesson in topic.lessons.all():
        cnt += steps_finished(lesson)

    return cnt


@register.filter
def topic_steps_cnt(topic):
    cnt = 0
    for lesson in topic.lessons.all():
        cnt += lesson.steps.count()

    return cnt


@register.simple_tag
def topic_progress_percent(topic):
    if topic_steps_cnt(topic) == 0:
        return 0

    return str(round(topic_progress(topic)/topic_steps_cnt(topic)*100))


@register.filter
def lesson_progress_percent(lesson):
    cnt = steps_counter(lesson)
    if cnt == 0:
        return 0

    return str(round(steps_finished(lesson)/cnt*100))


@register.simple_tag
def end_steps_count_for_topic(topic, user):
    cnt = 0
    cnt_2 = 0
    for lesson in topic.lessons.all():
        for step in lesson.steps.all():
            for enroll in step.steps_enrolls.all():
                if enroll.user == user and enroll.status == 'OK':
                    cnt += 1
            cnt_2 += 1

    return f'{cnt} / {cnt_2}'






# Новейшее'''


@register.simple_tag
def is_problem_correct(attempts):
    for attempt in attempts:
        if attempt.verdict == 'OK':
            return True
    return False


@register.filter
def point(time):
    return str(time).replace(',', '.')


# Еще новее. Точно последнее

@register.simple_tag
def get_width_col(lesson):
    cnt = lesson.connections.count()

    return 28 * cnt + 4 * (cnt - 1)
