from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from account.models import Team, Person
from team.forms import AddTeamForm, CreateTeamForm, DeleteTeamForm
from datetime import *


# Create your views here.

def team(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login/')
    context = {}
    if Person.objects.get(person=request.user).team is not None:
        score = Person.objects.get(person=request.user).team.score
        userTeamRank = Team.objects.filter(score__gte=score).count() + 1
        context = {
            'score': score,
            'userTeamRank': userTeamRank,
        }
    allTeamRank = Team.objects.order_by('-score')
    for t in allTeamRank:
        t.teammate = Person.objects.filter(team=t)
    context['allTeamRank'] = allTeamRank

    return render(request, 'team/teamIndex.html', context)


def teamAdd(request):
    res = False
    team_info = {}
    team_form = AddTeamForm()
    person = Person.objects.get(person=request.user)
    # 用户已经加入一支队伍
    if person.team:
        context = {
            'error': '您已经加入了一支队伍!',
            'forms': team_form,
            'res': res,
            'time_now': datetime.now(),
        }
        return render(request, 'team/teamAdd.html', context)

    if request.method == 'POST':
        team_form = AddTeamForm(data=request.POST)
        # 信息正确
        if team_form.is_valid():
            res = True
            team = Team.objects.get(id=team_form.cleaned_data['id'])
            team_info = {
                'team_name': team.teamName,
                'team_id': team.id,
                'team_score': team.score,
                'teammates': team.person_set.all()
            }

    context = {
        'forms': team_form,
        'res': res,
        'team_info': team_info,
        'time_now': datetime.now(),
    }
    context.update(team_info)
    return render(request, 'team/teamAdd.html', context)


def confirmAddTeam(request):
    if request.method == 'POST':
        team_form = AddTeamForm(data=request.POST)
        if team_form.is_valid():
            team_name = team_form.cleaned_data['teamName']
            team_id = team_form.cleaned_data['id']
            # status 0：无此队伍或者无此用户，1：成功，2：队伍人数已达到三人, 3:用户已经加入一支队伍
            try:
                person = Person.objects.get(person=request.user)
                team = Team.objects.get(teamName=team_name, id=team_id)
                if person.team:
                    return HttpResponse(3)
                if team.person_set.all().count() >= 3:
                    return HttpResponse(2)
                else:
                    person.team = team
                    person.save()
                    return HttpResponse(1)
            except:
                return HttpResponse(0)
        else:
            return HttpResponse(0)


def teamCreate(request):
    res = False
    team_form = CreateTeamForm()

    person = Person.objects.get(person=request.user)
    # 用户已经加入一支队伍
    if person.team:
        context = {
            'error': '您已经加入了一支队伍!',
            'forms': team_form,
            'res': res,
            'time_now': datetime.now(),
        }
        return render(request, 'team/teamCreate.html', context)

    if request.method == 'POST':
        team_form = CreateTeamForm(data=request.POST)
        # 信息正确
        if team_form.is_valid():
            team = Team.objects.create(teamName=team_form.cleaned_data['teamName'], score=0,
                                       email=team_form.cleaned_data['teamEmail'])
            person.team = team
            team.save()
            person.save()
            team_form = CreateTeamForm()
            res = True

    content = {
        'forms': team_form,
        'res': res,
        'time_now': datetime.now(),
    }
    return render(request, 'team/teamCreate.html', content)


def teamDelete(request):
    res = False
    delete_form = DeleteTeamForm()
    person = Person.objects.get(person=request.user)
    # 用户未加入一支队伍
    if not person.team:
        context = {
            'error': '您没有加入任何一支队伍!',
            'forms': delete_form,
            'res': res,
            'time_now': datetime.now(),
        }
        return render(request, 'team/teamDelete.html', context)

    if request.method == 'POST':
        delete_form = DeleteTeamForm(data=request.POST)
        # 信息正确
        if delete_form.is_valid():
            password = delete_form.cleaned_data["password"]
            user = authenticate(username=request.user.username, password=password)
            if user:
                person.team = None
                person.save()
                res = True
            else:
                context = {
                    'forms': delete_form,
                    'time_now': datetime.now(),
                    'error': '密码错误',
                }
                return render(request, 'team/teamDelete.html', context)

            delete_form = DeleteTeamForm()

    context = {
        'forms': delete_form,
        'res': res,
        'time_now': datetime.now(),
    }
    return render(request, 'team/teamDelete.html', context)
