from django.contrib.auth import authenticate, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

from account.forms import UserForm, BasePersonForm
from datetime import *
from .models import Person
from challenges.models import Solved, Problem, Team


# Create your views here.
def divide_pages(count, records_per_page, page_now):
    pages = count / records_per_page
    item_start = (page_now - 1) * records_per_page
    item_end = page_now * records_per_page

    if count % records_per_page != 0:
        pages += 1
    # 小于5页，只展示pages个分页
    if pages <= 5:
        page_range = range(1, pages + 1)
    # 大于5页且剩余页数大于5页，展示连续的5页
    elif pages - page_now + 1 >= 5:
        page_range = range(page_now, page_now + 5)
    # 大于5页且剩余页数少于5页，展示倒数5页
    else:
        page_range = range(pages - 4, pages + 1)

    return {
        'pages': pages,
        'page_range': page_range,
        'item_start': item_start,
        'item_end': item_end,
    }


@login_required
def profile(request):
    content = {
        'time_now': datetime.now(),
        'has_error': True,
        'error_content': '发生错误，请重试',
    }
    if request.user.is_authenticated:
        user = request.user
        try:
            person = Person.objects.get(person=user)
            user_score = person.score
            user_rank = Person.objects.filter(score__gte=user_score).count()

            team = person.team
            if team is None:
                content['team_name'] = ''
            else:
                team_score = team.score
                team_rank = Team.objects.filter(score__gte=team_score).count()-1
                content.update({
                    'team_id': team.id,
                    'team_name': team.teamName,
                    'team_rank': team_rank,
                    'team_score': team_score,
                })
            solves = Solved.objects.filter(res=True, user=person).order_by('-datetime_done')
            content.update({
                'time_now': datetime.now(),
                'has_error': False,
                'error_content': '发生错误，请重试',
                'solves': solves,
                'person': person,
                'user_rank': user_rank,
            })
            return render(request, 'account/profile.html', content)
        except:
            content['error_content'] = '无此用户'
            return render(request, 'account/profile.html', content)


@login_required
def setting(request):
    content = {
        'time_now': datetime.now(),
        'has_error': False,
        'error_content': '',
        'change': False
    }
    if request.method == 'GET':
        return render(request, 'account/setting.html', content)

    if request.user.is_authenticated:
        user = request.user
        username = user.username
        currentPsd = request.POST.get('currentPsd')
        newPsd = request.POST.get('newPsd')
        confirmNewPsd = request.POST.get('confirmNewPsd')
        if authenticate(username=username, password=currentPsd) is None:
            content['has_error'] = True
            content['error_content'] = '原密码输入错误'
            return render(request, 'account/setting.html', content)
        if len(newPsd) < 6 or len(newPsd) > 18:
            content['has_error'] = True
            content['error_content'] = '请输入6-18位密码'
            return render(request, 'account/setting.html', content)
        if newPsd != confirmNewPsd:
            content['has_error'] = True
            content['error_content'] = '两次输入的密码不一致'
            return render(request, 'account/setting.html', content)
        user.set_password(newPsd)
        user.save()
        login(request, user)
        content['has_error'] = False
        content['change'] = True
        return render(request, 'account/setting.html', content)


def feedback(request):
    return render(request, 'account/feedback.html', {'time_now': datetime.now()})


def login_user(request):
    content = {
        'has_error': False,
        'error_content': '',
        'time_now': datetime.now(),
    }
    # POST 发送注册信息
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                content['has_error'] = True
                content['error_content'] = '该账号已被冻结'
                return render(request, 'account/login.html', content)
        else:
            content['has_error'] = True
            content['error_content'] = '账号或者密码错误'
            return render(request, 'account/login.html', content)

    return render(request, 'account/login.html', content)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    registered = False
    # POST 发送注册信息
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        person_form = BasePersonForm(data=request.POST)

        # 信息正确
        if user_form.is_valid() and person_form.is_valid():
            user = user_form.save()
            # hash密码
            user.set_password(user.password)
            user.is_active = True

            person = person_form.save(commit=False)
            person.person = user

            user.save()
            person.save()

            user_form = UserForm()
            person_form = BasePersonForm()
            registered = True

    else:
        user_form = UserForm()
        person_form = BasePersonForm()

    content = {
        'forms': (user_form, person_form,),
        'registered': registered,
        'time_now': datetime.now(),
    }

    return render(request, 'account/register.html', content)
