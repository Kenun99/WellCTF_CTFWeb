from django.shortcuts import render
from django.http import HttpResponse
from .models import Problem, Contest, Solved
from account.models import Person
from datetime import *


def get_rank(user):
    score = Person.objects.get(person=user).score
    user_rank = Person.objects.filter(score__gte=score).count()
    top_ten = Person.objects.order_by('-score')[:10]

    content = {
        'top_ten': top_ten,
        'user_rank': user_rank,
        'socre': score,
    }
    return content


def contests(request):
    contests = Contest.objects.all()
    content = {
        'contests': contests,
        'time_now': datetime.now(),
    }
    rank_info = get_rank(request.user)
    content.update(rank_info)
    return render(request, 'challenges/contests.html', content)


def contest_detail(request, contest_id):
    content = {
        'detail': '无',
        'problems': [],
        'time_now': datetime.now()
    }
    rank_info = get_rank(request.user)
    content.update(rank_info)
    if request.method == 'GET':
        contest_id = int(contest_id)
        contest = Contest.objects.get(id=contest_id)
        detail = contest.detail
        problems = contest.problem_set.all()

        content.update({
            'detail': detail,
            'problems': problems,
            'time_now': datetime.now(),
            'begin': contest.datetime_begin,
            'end': contest.datetime_end,
            'timeLen': contest.datetime_end - contest.datetime_begin,
            'contest_id': contest_id,
        })
        return render(request, 'challenges/contest_detail.html', content)


def get_problems(request, type=0):
    kind = ['全部', 'Web', '密码学', '安全杂项', '逆向工程', '隐写术', '编程', '溢出']
    type = int(type)
    if type == 0:
        problems = Problem.objects.filter(type__gte=type)
    else:
        problems = Problem.objects.filter(type=type)
    content = {
        'kind': kind,
        'problems': problems,
        'time_now': datetime.now(),
        'type': type,
    }
    rank_info = get_rank(request.user)
    content.update(rank_info)
    return render(request, 'challenges/problems.html', content)


def flagPost(request):
    # status. 0: 答案错误，1:答案正确， 2:输入为空
    status = 2
    res = 0
    if request.method == 'POST':
        person = Person.objects.get(person=request.user)
        problem_id = request.POST.get('problem_id')
        contest_id = request.POST.get('contest_id')
        problem = Problem.objects.get(id=problem_id)
        flag_ans = problem.flag
        if request.POST.get('flag') == '':
            status = 2
            res = 0
        elif flag_ans == request.POST.get('flag'):
            status = 1
            res = 1

            person.score = person.score + problem.bill
            person.save()
        else:
            res = 0
            status = 0
        Solved.objects.create(user_id=person.id, problem_id=problem_id, contest_id=contest_id, res=res,
                              datetime_done=datetime.now())
        return HttpResponse(status)
    return HttpResponse(status)
