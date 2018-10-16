from django.contrib import admin
from account.models import Person

# Register your models here.

admin.site.site_header = 'WellCTF后台管理'
admin.site.site_title = 'WellCTF'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('person', 'gender', 'institute', 'score')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # 操作项功能显示位置设置，两个都为True则顶部和底部都显示
    actions_on_top = True
    # 操作项功能显示选中项的数目
    actions_selection_counter = True
    # 字段为空值显示的内容
    empty_value_display = ' -空白- '
