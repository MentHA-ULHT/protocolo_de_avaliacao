from django import forms
from django.forms import ModelForm

from .models import *


class uploadAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text_answer', 'quotation', 'notes', 'submitted_answer']
        # text_answer = forms.Textarea(max_length=LONG_LEN, required=True)
        # quotation = forms.ModelMultipleChoiceField(queryset=Answer.objects.all())
        # notes = forms.Textarea(max_length=LONG_LEN, required=False)
        # submitted_answer = forms.ImageField(required=False)
