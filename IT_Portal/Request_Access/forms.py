from django import forms
from .models import *


class RequestForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'



class AccessForm(forms.ModelForm):
    class Meta:
        model = Access
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'