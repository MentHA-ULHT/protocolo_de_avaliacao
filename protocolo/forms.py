from django import forms
from django.forms import ModelForm

from .models import *


class uploadAnswerForm(ModelForm):
    class Meta:
        model = Answer

        fields = ['text_answer', 'quotation', 'notes','submitted_answer']
        widgets = {
            'text_answer': forms.Textarea(attrs={'rows': 3, 'cols': 0, 'class': 'notes-area form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 0, 'class': 'notes-area form-control'}),
        }

        labels = {'text_answer': 'Resposta escrita (se necessário):',
                  'quotation': 'Cotação',
                  'notes': 'Apontamentos',
                  'submitted_answer': 'Submeta uma fotografia'
                  }

        def __init__(self, *args, **kwargs):
            super(uploadAnswerForm, self).__init__(*args, **kwargs)
            self.fields['submitted_answer'].required = False
            self.fields['notes'].required = False

        # text_answer = forms.Textarea(max_length=LONG_LEN, required=True)
        # quotation = forms.ModelMultipleChoiceField(queryset=Answer.objects.all())
        # notes = forms.Textarea(max_length=LONG_LEN, required=False)
        # submitted_answer = forms.ImageField(required=False)
