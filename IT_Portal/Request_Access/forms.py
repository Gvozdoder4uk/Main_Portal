from django import forms
from .models import *
from django.forms import inlineformset_factory

SERVICES = (
    (1, "АСУ ВП"),
    (2, "1С Русагротранс"),
    (3, "АСУ ТК"),
    (4, "Файловое Хранилище"),
    (5, "Удаленный доступ"),
    (6, "Русагротранс Онлайн"),

)


class AccessForm(forms.ModelForm):
    class Meta:
        model = Access
        exclude = ('number_task',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['name_user'].widget.attrs['class'] = 'form-control'
            self.fields['user_dep'].widget.attrs['class'] = 'form-control'
            self.fields['user_otdel'].widget.attrs['class'] = 'form-control'
            self.fields['request_desc'].widget.attrs['class'] = 'form-control'


from .models import Mails


class EmailForm(forms.ModelForm):
    email = forms.EmailField(max_length=200,
                             widget=forms.TextInput(attrs={'class': "form-control", 'id': "clientemail"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Mails
        fields = ('email', 'subject', 'message',)


class ApproveForm(forms.ModelForm):
    email_service_owner = forms.EmailField(max_length=200)
    email_boss = forms.EmailField(max_length=200)
    email_ib = forms.EmailField(max_length=200)
    email_fileserver = forms.EmailField(max_length=200, required=False)
    fileserver_owner = forms.EmailField(required=False)

    class Meta:
        model = ApproveList
        fields = '__all__'
        widgets = {'': forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['service_owner'].widget.attrs['class'] = 'form-control'
            self.fields['email_boss'].widget.attrs['class'] = 'form-control'
            self.fields['email_service_owner'].widget.attrs['class'] = 'form-control'
            self.fields['email_boss'].widget.attrs['readonly'] = False
            self.fields['email_ib'].widget.attrs['readonly'] = True
            self.fields['email_service_owner'].widget.attrs['readonly'] = True
            self.fields['email_fileserver'].widget.attrs['readonly'] = True


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('address',)
