#-*- coding=utf-8 -*-

from django import forms
from .models.eduModels import Student
#from django.forms.widgets import TextInput,PasswordInput

class LoginForm(forms.Form):

    studentid = forms.CharField(widget=forms.TextInput(attrs = {
            'name':'studentid',
            'class':'form-control',
            'placeholder':u'请输入学号'})
            )
    password = forms.CharField(widget=forms.PasswordInput(attrs = {
            'name':'password',
            'class':'form-control',
            'placeholder':u'密码'})
)
