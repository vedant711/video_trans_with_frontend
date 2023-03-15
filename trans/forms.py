from django import forms
from datetime import datetime

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()
    # date = forms.CharField(max_length=150, initial=datetime.now(),disabled=True,label='',widget=forms.HiddenInput)