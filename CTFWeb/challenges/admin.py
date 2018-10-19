from django.contrib import admin
from challenges.models import Problem, Contest, Solved, CompeteMsg


# Register your models here.

admin.site.register(CompeteMsg)
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'bill', 'type', 'flag')
    list_per_page = 50
    actions_on_top = True
    empty_value_display = ' -空白- '
    search_fields = ('name', 'id', 'type')


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime_begin', 'datetime_end')
    list_per_page = 50
    actions_on_top = True
    empty_value_display = ' -空白- '
    search_fields = ('name', 'datetime_begin')


@admin.register(Solved)
class SolvedAdmin(admin.ModelAdmin):
    list_display = ('problem_id', 'user_id', 'res', 'datetime_done')
    list_per_page = 50
    actions_on_top = True
    empty_value_display = ' -空白- '
    search_fields = ('problem_id', 'res')
