from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput
import re
from account.models import Person

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
        re_password = re.compile('^[a-zA-Z]\w{5,17}$')
        if password != confirm_password:
            raise forms.ValidationError('两次密码不一致')
        if (not re_password.match(password)) or (not re_password.match(confirm_password)):
            raise forms.ValidationError('密码以字母开头，只能包含字母、数字和下划线')
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

    captcha = CaptchaField(
        label='验证码',
        widget=CaptchaTextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入验证码'},
        ),
        error_messages={
            "invalid": u"验证码错误",
            "required": u"请输入验证码",
        }
    )

    class Meta:
        model = Person
        fields = ('gender', 'institute', 'captcha')


