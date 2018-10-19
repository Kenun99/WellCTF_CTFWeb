from django.shortcuts import render
from django.http import HttpResponse
from .models import Problem, Contest, Solved, CompeteMsg
from account.models import Person, Team
from datetime import *

rank = {}


def get_rank(user):
    score = Person.objects.get(person=user).score
    user_rank = Person.objects.filter(score__gte=score).count()
    top_ten = Person.objects.order_by('-score')[:10]
    global rank
    rank = {
        'top_ten': top_ten,
        'user_rank': user_rank,
        'socre': score,
    }


def contests(request):
    contests = Contest.objects.all()
    content = {
        'contests': contests,
        'time_now': datetime.now(),
    }

    if not rank:
        get_rank(request.user)
    content.update(rank)  # 添加全站排名
    return render(request, 'challenges/contests.html', content)


def contest_detail(request, contest_id):
    content = {
        'currentPage': 'contest_detail',
        'detail': '无',
        'problems': [],
        'time_now': datetime.now()
    }
    if not rank:
        get_rank(request.user)
    content.update(rank)

    contest_id = int(contest_id)
    contest = Contest.objects.get(id=contest_id)
    detail = contest.detail
    problems = contest.problem_set.all()

    person = Person.objects.get(person=request.user)
    msg = CompeteMsg.objects.filter(player=person, contest=contest)
    if not msg:
        CompeteMsg.objects.create(player=person, contest=contest, score=0)

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


def board(request, contest_id):
    content = {
        'contest_id': contest_id,
        'currentPage': 'board',
    }
    user = request.user
    if user.is_authenticated:
        # 全站Rank
        if not rank:
            get_rank(request.user)
        content.update(rank)

        contest = Contest.objects.get(id=contest_id)
        datetime_begin = contest.datetime_begin
        datetime_end = contest.datetime_end
        content.update({
            'time_now': datetime.now(),
            'begin': datetime_begin,
            'end': datetime_end,
            'timeLen': datetime_end - datetime_begin,
        })
        # isTeam = contest.isTeam

        # 这场比赛每道题目的一血，二血，三血
        blood = []
        problems = contest.problem_set.all()
        for problem in problems:
            temp = {
                'solves': Solved.objects.filter(contest=contest, problem=problem, res=True).order_by('datetime_done'),
                'problem': problem,
            }
            blood.append(temp)
        content['blood'] = blood

        # 本比赛Rank情况
        msgs = CompeteMsg.objects.filter(contest=contest).order_by('-score')

        content['msgs'] = msgs

        # TODO
        # 各题目完成情况
        # result = []
        # for msg in msgs:
        #     solves = Solved.objects.filter(user=msg.player, res=True, contest=contest)
        #     temp = {
        #         'player': ,
        #         'solves': solves,
        #     }
        #     result.append(temp)

    return render(request, 'challenges/board.html', content)


def get_problems(request, type=0):
    get_rank(request.user)

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
    if not rank:
        get_rank(request.user)
    content.update(rank)
    return render(request, 'challenges/problems.html', content)


def flagPost(request):
    # status. 0: 答案错误，1:答案正确， 2:输入为空
    status = 2
    if request.method == 'POST':
        person = Person.objects.get(person=request.user)
        contest = Contest.objects.get(id=int(request.POST.get('contest_id')))
        problem = Problem.objects.get(id=int(request.POST.get('problem_id')))
        # team = person.team

        flag_ans = problem.flag
        if request.POST.get('flag') == '':
            status = 2
            res = False
        elif flag_ans == request.POST.get('flag'):
            status = 1
            res = True
        else:
            res = False
            status = 0

        passProblem = Solved.objects.filter(problem=problem, user=person, contest=contest)
        if not res:
            Solved.objects.create(user=person, problem=problem, contest=contest, res=False,
                                  datetime_done=datetime.now())

        # 用户未完成过此题目
        if res and (not passProblem.filter(res=True)):
            person.score = person.score + problem.bill
            person.save()

            # 比赛模式，参赛单位是否完成过此题目
            try:
                msg = CompeteMsg.objects.get(player=person, contest=contest)
                if msg:
                    msg.score = msg.score + problem.bill
                    team = Team.objects.get(id=msg.player.team.id)
                    team.score = team.score + problem.bill
                    team.save()
                    msg.save()
            except:
                pass
            Solved.objects.create(user=person, problem=problem, contest=contest, res=True,
                                  datetime_done=datetime.now())

    return HttpResponse(status)
