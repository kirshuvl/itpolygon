from django_project.celery import app
import epicbox
from lms.problems.models import TestForProblemStep, TestUserAnswer, UserAnswerForProblemStep
from lms.steps.models import StepEnroll


@app.task
def run_user_code(user_answer_pk):
    user_answer = UserAnswerForProblemStep.objects.get(pk=user_answer_pk)

    epicbox.configure(
        profiles=[
            epicbox.Profile('python', 'python:3.6.5-alpine')
        ]
    )

    if user_answer.problem.start_code != '':
        code = user_answer.problem.start_code.replace(
            '{{ user_code }}', user_answer.code)
    else:
        code = user_answer.code

    files = [
        {
            'name': 'main.py',
            'content': bytes(code, encoding='UTF-8')
        }
    ]
    limits = {
        'cputime': user_answer.problem.cputime,
        'memory': user_answer.problem.memory
    }

    tests = TestForProblemStep.objects.\
        filter(problem=user_answer.problem, number__gte=user_answer.problem.first_test).\
        order_by('number')

    data = []
    for num, test in enumerate(tests):
        result = epicbox.run(
            'python', 'python3 main.py',
            stdin=bytes(test.input, encoding='UTF-8'),
            files=files,
            limits=limits
        )
        data.append(
            TestUserAnswer(
                user=user_answer.user,
                code=user_answer,
                test=test,
                verdict=get_verdict(test, result),
                exit_code=result['exit_code'],
                stdout=str(result['stdout'], encoding='UTF-8'),
                stderr=str(result['stderr'], encoding='UTF-8').strip(),
                duration=result['duration'],
                timeout=result['timeout'],
                oom_killed=result['oom_killed'],
            )
        )

    verdict = ''
    for attempt in data:
        if attempt.verdict != 'OK':
            verdict = attempt.verdict
            break
    else:
        verdict = 'OK'

    cnt = 0
    for attempt in data:
        if attempt.verdict == 'OK':
            cnt += 1

    cpu_max = 0
    for attempt in data:
        cpu_max = max(cpu_max, attempt.duration)

    first_fail = 0
    for num, attempt in enumerate(data):
        if attempt.verdict != 'OK':
            first_fail = num + 1
            break

    user_answer.points = cnt
    user_answer.cputime = cpu_max
    user_answer.verdict = verdict
    user_answer.first_fail_test = first_fail

    step_enroll = StepEnroll.objects.get(
        user=user_answer.user, step=user_answer.problem)
    if step_enroll.status == 'PR':
        if verdict == 'OK':
            step_enroll.status = 'OK'
        else:
            step_enroll.status = 'WA'
    else:
        if verdict == 'OK':
            step_enroll.status = 'OK'

    TestUserAnswer.objects.bulk_create(data)
    user_answer.save()
    user_answer.user.save()
    step_enroll.save()


def get_verdict(test, result):
    res = str(result['stdout'], encoding='UTF-8')

    if result['timeout']:
        return 'TL'
    elif result['oom_killed']:
        return 'ML'
    elif result['stderr'] != b'':
        return 'CE'
    elif [line.strip() for line in test.output.split('\n')] != res.split('\n'):
        return 'WA'
    elif [line.strip() for line in test.output.split('\n')] == res.split('\n'):
        return 'OK'
    return 'UN'
