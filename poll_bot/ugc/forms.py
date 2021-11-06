from typing import Text
from django import forms
from django.forms import fields, widgets

from .models import Answers, Language, Profile, Question, RightAnswers

class ProfileForm(forms.ModelForm):
    model = Profile
    fields = (
        'external_id',
        'language',
        'wallet',
        'chosen_ques',
        'chosen_ans',
    )
    widgets = {
        'language': forms.TextInput,
    }

class LanguageForm(forms.ModelForm):
    model = Language
    fields = (
        'greeting',
        'selected_lang',
        'profile',
        'post',
        'wallet',
        'ans_ques',
        'question',
    )
    widgets = {
        'selected_lang': forms.TextInput
    }

class QuestionForm(forms.ModelForm):
    model = Question
    fields = (
        'name',
        'right_choice',
        'number'
        'status'
    )

    statuses = [('Active','Active'), ('Inactive','Inactive'),]

    #Adds choice field in order to change the status
    def __init__(self, *args, **kwargs):
       super(QuestionForm, self).__init__(*args, **kwargs)
       if self.instance.id:
           self.fields['status'] = forms.ChoiceField(
                choices= self.statuses)

class RightAnswersForm(forms.ModelForm):
    model = RightAnswers
    fields=(
        'question',
        'name',
        'phone',
        'user_id',
        'answer',
        'number',
        'send_money'
        )
    CHOICES = [(True,True,),(False,False)]

    send_money = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
