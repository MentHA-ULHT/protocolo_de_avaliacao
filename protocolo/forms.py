from django import forms
from .models import *


class uploadAnswerForm(forms.Form):
    class Meta:
        fields = '__all__'
        # text_answer = forms.Textarea(max_length=LONG_LEN, required=True)
        # quotation = forms.ModelMultipleChoiceField(queryset=Answer.objects.all())
        # notes = forms.Textarea(max_length=LONG_LEN, required=False)
        # submitted_answer = forms.ImageField(required=False)