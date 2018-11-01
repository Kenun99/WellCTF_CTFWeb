from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problem, Contest, Solved, CompeteMsg
from account.models import Person
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login/')
    contests = Contest.objects.all()[1::]
    content = {
        'contests': contests,
        'time_now': datetime.now(),
    }
    if not rank:
        get_rank(request.user)
    content.update(rank)  # 添加全站排名
    return render(request, 'challenges/contests.html', content)


def contest_detail(request, contest_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login/')
    contest_id = int(contest_id)
    contest = Contest.objects.get(id=contest_id)
    person = Person.objects.get(person=request.user)
    content = {
        'detail': '无',
        'problems': [],
        'currentPage': 'contest_detail',
        'time_now': datetime.now(),
        'begin': contest.datetime_begin,
        'end': contest.datetime_end,
        'timeLen': contest.datetime_end - contest.datetime_begin,
        'contest_id': contest_id,
    }
    if not rank:
        get_rank(request.user)
    content.update(rank)
    # 未加入队伍的不能参加团体赛
    if contest.isTeam and (not person.team):
        content.update({
            'error': '您未加入任何一支队伍，无法参加团体赛'
        })
        return render(request, 'challenges/contest_detail.html', content)
    # 记录参加比赛的选手
    if contest.isTeam:
        msg = CompeteMsg.objects.filter(team=person.team, contest=contest).count()
        if msg is 0:
            CompeteMsg.objects.create(team=person.team, contest=contest, score=0)
    else:
        msg = CompeteMsg.objects.filter(player=person, contest=contest).count()
        if msg is 0:
            CompeteMsg.objects.create(player=person, contest=contest, score=0)

    detail = contest.detail
    problems = contest.problem_set.all()
    content.update({
        'detail': detail,
        'problems': problems,
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
            'isTeam': contest.isTeam,
            'time_now': datetime.now(),
            'begin': datetime_begin,
            'end': datetime_end,
            'timeLen': datetime_end - datetime_begin,
        })

        # 这场比赛每道题目的一血，二血，三血
        blood = []
        problems = contest.problem_set.all()
        for problem in problems:
            temp = {
                'solves': Solved.objects.filter(contest=contest, problem=problem, res=True).order_by('datetime_done')[
                          0:3],
                'problem': problem,
            }
            print(temp['solves'])
            blood.append(temp)
        content['blood'] = blood

        # 本比赛Rank情况
        msgs = CompeteMsg.objects.filter(contest=contest).order_by('-score')

        content['msgs'] = msgs

        # 各题目完成情况 TODO

    return render(request, 'challenges/board.html', content)


def get_problems(request, type=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login/')
    get_rank(request.user)
    kind = ['全部', 'Web', '密码学', '安全杂项', '逆向工程', '隐写术', '编程', '溢出']
    type = int(type)
    if type == 0:
        problems = Problem.objects.filter(type__gte=type)
    else:
        problems = Problem.objects.filter(type=type)
    person = Person.objects.get(person=request.user)
    for p in problems:
        if Solved.objects.filter(user=person, problem=p):
            p.isdone = True

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
        problem = Problem.objects.get(id=int(request.POST.get('problem_id')))
        contest = problem.contest

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

        if contest.isTeam:
            pass_problem = Solved.objects.filter(problem=problem, team=person.team, contest=contest)
            # 记录回答错误
            if not res:
                Solved.objects.create(user=person, problem=problem, contest=contest, res=False,
                                      datetime_done=datetime.now(), team=person.team)
        else:
            pass_problem = Solved.objects.filter(problem=problem, user=person, contest=contest)
            # 记录回答错误
            if not res:
                Solved.objects.create(user=person, problem=problem, contest=contest, res=False,
                                      datetime_done=datetime.now())

        # 回答正确，处理加分。用户未完成过此题目
        if res and (not pass_problem.filter(res=True)):
            person.score = person.score + problem.bill
            person.save()
            # 团队比赛模式
            if contest.isTeam:
                msg = CompeteMsg.objects.filter(team=person.team, contest=contest)
            else:
                # 个人比赛模式
                msg = CompeteMsg.objects.filter(player=person, contest=contest)
            # 参赛队伍是否完成过此题目
            if msg.count() is not 0:
                msg = msg[0]
                msg.score = msg.score + problem.bill
                msg.save()

                team = person.team
                if team is not None:
                    team.score = team.score + problem.bill
                    team.save()

            Solved.objects.create(user=person, problem=problem, contest=contest, res=True,
                                  datetime_done=datetime.now())

    return HttpResponse(status)
