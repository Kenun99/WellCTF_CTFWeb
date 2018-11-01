from django.core.exceptions import ValidationError
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
import re
from account.models import Team


def delete_team_exit_validate(value):
    username_re = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{2,9}$')
    if not username_re.match(value):
        raise ValidationError('队伍名只允许含有字母、数字和下划线')
    elif Team.objects.filter(teamName=value).exists():
        raise ValidationError('该队伍已存在')


def add_team_exit_validate(value):
    team_name_re = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{2,9}$')
    if not team_name_re.match(value):
        raise ValidationError('队伍名只允许含有字母、数字和下划线')
    elif not Team.objects.filter(teamName=value).exists():
        raise ValidationError('该队伍不存在')


def add_team_id_exit_validate(value):
    if type(value) is 'number':
        raise ValidationError('数字')
    elif not Team.objects.filter(id=value).exists():
        raise ValidationError('该队伍不存在')


def team_email_validate(value):
    teamname_re = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    if not teamname_re.match(value):
        raise ValidationError('无效的 Email 格式！')
    if Team.objects.filter(email=value).exists():
        raise ValidationError('该Email已经被其他队伍使用！')


class AddTeamForm(forms.Form):
    teamName = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入队伍名字'}
        ),
        validators=[add_team_exit_validate],
        error_messages={
            'required': '请填写队伍名字',
            'max_length': '队伍名不得多于8位字符',
            'min_length': '队伍名不得少于3位字符',
        },
        label='队伍名',
        max_length=10,
        min_length=3,
        required=True
    )
    id = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': '请输入队伍ID'}
        ),
        label='队伍ID',
        validators=[add_team_id_exit_validate],
        required=True,
        error_messages={
            'required': '请填写队伍ID',
        },
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


class CreateTeamForm(forms.ModelForm):
    teamName = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入队伍名字'}
        ),
        validators=[delete_team_exit_validate],
        error_messages={
            'required': '请填写队伍名字',
            'max_length': '队伍名不得多于10位字符',
            'min_length': '队伍名不得少于3位字符',
        },
        label='队伍名',
        max_length=10,
        min_length=3,
        required=True

    )
    teamEmail = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入队伍Email'}
        ),
        validators=[team_email_validate],
        error_messages={
            'required': '请填写队伍Email',
            'max_length': 'Email不得多于30位字符',
            'min_length': 'Email不得少于5位字符',
        },
        label='队伍Email',
        max_length=30,
        min_length=5,
        required=True
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

    # 验证队伍存在性
    def clean_team_name(self):
        cleaned_data = super(CreateTeamForm, self).clean()
        teamName = cleaned_data.get('teamName')
        teamEmail = cleaned_data.get('teamEmail')

        team = Team.objects.filter(teamName=teamName)
        if team:
            raise forms.ValidationError(u'此队伍已经被使用')
        team = Team.objects.filter(email=teamEmail)
        if team:
            raise forms.ValidationError(u'此Email已经被使用')
        return cleaned_data

    class Meta:
        model = Team
        fields = ('teamName', 'teamEmail', 'captcha')


class DeleteTeamForm(forms.ModelForm):
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

    # 验证密码
    def clean_confirm_password(self):
        cleaned_data = super(DeleteTeamForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('两次密码不一致')
        return cleaned_data

    class Meta:
        model = Team
        fields = ('password', 'confirm_password')
