from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields, widgets
from django.contrib.auth.models import User
import re
from django.core.validators import RegexValidator
from account.models import Person


# class registerForm(forms.Form):
#     username = fields.CharField(
#         required=True,
#         widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户名为8-12个字符'}),
#         min_length=4,
#         max_length=12,
#         strip=True,
#         error_messages={'required': '标题不能为空',
#                         'min_length': '用户名最少为4个字符',
#                         'max_length': '用户名最不超过为12个字符'},
#     )
#     gender = forms.CharField(
#         widget=forms.Select(
#             choices=((u'男', '男'), (u'女', '女')),
#             attrs={'class': 'form-control', 'placeholder': '请选择性别'},
#         ),
#         label='性别',
#         max_length=8,
#         required=True,
#         error_messages={
#             'required': '请选择性别'
#         }
#     )
#     institute = forms.CharField(
#         widget=forms.Select(
#             choices=(
#                 ('信息与通信工程学院', '信息与通信工程学院'),
#                 ('电子工程学院', '电子工程学院'),
#                 ('计算机学院', '计算机学院'),
#                 ('自动化学院', '自动化学院'),
#                 ('数字媒体与设计艺术学院', '数字媒体与设计艺术学院'),
#                 ('现代邮政学院', '现代邮政学院'),
#                 ('网络空间安全学院', '网络空间安全学院'),
#                 ('光电信息学院', '光电信息学院'),
#                 ('理学院', '理学院'),
#                 ('经济管理学院', '经济管理学院'),
#                 ('公共管理学院', '公共管理学院'),
#                 ('人文学院', '人文学院'),
#                 ('国际学院', '国际学院'),
#                 ('软件学院', '软件学院'),
#             ),
#             attrs={'class': 'form-control', 'placeholder': '请选择学院'},
#         ),
#         label='学院',
#         max_length=15,
#         required=True,
#         error_messages={
#             'required': '请选择学院'
#         }
#     )
#     pwd = fields.CharField(
#         widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请输入密码，必须包含数字,字母,特殊字符'},
#                                      render_value=True),
#         required=True,
#         min_length=6,
#         max_length=20,
#         strip=True,
#         validators=[
#             RegexValidator(r'((?=.*\d))^.{6,20}$', '必须包含数字'),
#             RegexValidator(r'((?=.*[a-zA-Z]))^.{6,20}$', '必须包含字母'),
#             RegexValidator(r'^.(\S){6,20}$', '密码不能包含空白字符'),
#         ],  # 用于对密码的正则验证
#         error_messages={'required': '密码不能为空!',
#                         'min_length': '密码最少为6个字符',
#                         'max_length': '密码最多不超过为12个字符!',
#                         'invalid': '密码必须包含数字、字母且不能包含空格'},
#     )
#     pwd_again = fields.CharField(
#         # render_value会对于PasswordInput，错误是否清空密码输入框内容，默认为清除，我改为不清楚
#         widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请再次输入密码!'}, render_value=True),
#         required=True,
#         strip=True,
#         error_messages={'required': '请再次输入密码!', }
#     )
#
#     def clean_username(self):
#         # 对username的扩展验证，查找用户是否已经存在
#         username = self.cleaned_data.get('username')
#         users = User.objects.filter(username=username).count()
#         if users:
#             raise ValidationError('用户已经存在！')
#         return username
#
#     def clean_email(self):
#         # 对email的扩展验证，查找用户是否已经存在
#         email = self.cleaned_data.get('email')
#         email_count = User.objects.filter(email=email).count()  # 从数据库中查找是否用户已经存在
#         if email_count:
#             raise ValidationError('该邮箱已经注册！')
#         return email
#
#     def _clean_new_password2(self):  # 查看两次密码是否一致
#         password1 = self.cleaned_data.get('pwd')
#         password2 = self.cleaned_data.get('pwd_again')
#         if password1 and password2:
#             if password1 != password2:
#                 # self.error_dict['pwd_again'] = '两次密码不匹配'
#                 raise ValidationError('两次密码不匹配！')
#
#     def clean(self):
#         # 是基于form对象的验证，字段全部验证通过会调用clean函数进行验证
#         self._clean_new_password2()  # 简单的调用而已


def username_validate(value):
    username_re = re.compile(r'^20[0-4][0-9](21|66|52|11|81)\d{4}$')
    if not username_re.match(value):
        raise ValidationError('学号格式错误')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('该账户已存在')


class UserForm(forms.ModelForm):
    # field password override that in Person
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入6-18位密码'}
        ),
        min_length=6,
        max_length=18,
        label="密码",
        required=True,
        error_messages={
            'required': '请输入密码',
            'min_length': '密码过短',
            'max_length': '密码过长',
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}
        ),
        min_length=6,
        max_length=18,
        label="重复密码",
        required=True,
        error_messages={
            'required': '请再次输入密码',
            'min_length': '密码过短',
            'max_length': '密码过长',
        }
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入10位学号'}
        ),
        validators=[username_validate],
        error_messages={
            'required': '请填写学号',
            'max_lengh': '请输入10位完整学号',
            'min_length': '请输入10位完整学号',
        },
        label='学号',
        max_length=10,
        min_length=10,
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'}),
        label='姓名',
        required=True,
        max_length=15,
        error_messages={
            'required': '请输入姓名',
            'max_length': '姓名过长',
        }
    )

    # 验证密码
    def clean_confirm_password(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('两次密码不一致')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password', 'confirm_password',)


class BasePersonForm(forms.ModelForm):
    gender = forms.CharField(
        widget=forms.Select(
            choices=((u'男', '男'), (u'女', '女')),
            attrs={'class': 'form-control', 'placeholder': '请选择性别'},
        ),
        label='性别',
        max_length=8,
        required=True,
        error_messages={
            'required': '请选择性别'
        }
    )
    institute = forms.CharField(
        widget=forms.Select(
            choices=(
                (u'信息与通信工程学院', '信息与通信工程学院'),
                (u'电子工程学院', '电子工程学院'),
                (u'计算机学院', '计算机学院'),
                (u'自动化学院', '自动化学院'),
                (u'数字媒体与设计艺术学院', '数字媒体与设计艺术学院'),
                (u'现代邮政学院', '现代邮政学院'),
                (u'网络空间安全学院', '网络空间安全学院'),
                (u'光电信息学院', '光电信息学院'),
                (u'理学院', '理学院'),
                (u'经济管理学院', '经济管理学院'),
                (u'公共管理学院', '公共管理学院'),
                (u'人文学院', '人文学院'),
                (u'国际学院', '国际学院'),
                (u'软件学院', '软件学院'),
            ),
            attrs={'class': 'form-control', 'placeholder': '请选择学院'},
        ),
        label='学院',
        max_length=15,
        required=True,
        error_messages={
            'required': '请选择学院'
        }
    )

    class Meta:
        model = Person
        fields = ('gender', 'institute')


