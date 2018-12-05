from django.shortcuts import render
from datetime import *
from challenges.models import Solved
from account.models import Person
from challenges.views import get_rank


# Create your views here.

def index(request):
    # 今日提交
    todayDate = datetime.now().date() + timedelta(days=0)  # 今天
    solveBase = Solved.objects.filter(datetime_done__contains=todayDate)
    # 今日提交总数
    pushAllToday = solveBase.count()
    # 正确提交总数
    solvedToday = solveBase.filter(res=True)
    pushAllTrueToday = solvedToday.count()
    # 今日得分
    scoreAllToday = 0
    for each in solvedToday:
        scoreAllToday = scoreAllToday + each.problem.bill
    context = {
        'scoreAllToday': scoreAllToday,
        'pushAllToday': pushAllToday,
        'pushAllTrueToday': pushAllTrueToday,
        'time_now': datetime.now(),
        'top_ten': Person.objects.order_by('-score')[:10]
    }
    return render(request, 'index.html', context)
