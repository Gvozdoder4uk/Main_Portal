from django import forms
from .models import *
from django.forms import inlineformset_factory
from django.contrib.admin.widgets import FilteredSelectMultiple

SERVICES = (
    (1, "АСУ ВП"),
    (2, "1С Русагротранс"),
    (3, "АСУ ТК"),
    (4, "Файловое Хранилище"),
    (5, "Удаленный доступ"),
    (6, "Русагротранс Онлайн"),

)

STATUS_SELECTOR = (
    ("Согласовано", "Согласовано"),
    ("Не согласовано", "Не согласовано")
)


class ApproveChanger(forms.Form):
    approve_choicer = forms.ChoiceField(choices=STATUS_SELECTOR)


class AccessForm(forms.ModelForm):
    user_name = forms.CharField(max_length=200)

    class Meta:
        model = Access
        exclude = ('number_task',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['request_statuser'].widget = forms.HiddenInput()
            self.fields['creator'].widget = forms.HiddenInput()
            self.fields['approve_list'].widget = forms.HiddenInput()
            self.fields['author'].widget = forms.HiddenInput()
            self.fields['user_name'].widget.attrs['class'] = 'form-control'
            self.fields['user_name'].widget.attrs['id'] = 'userfield'
            self.fields['user_dep'].widget.attrs['class'] = 'form-control'
            self.fields['user_otdel'].widget.attrs['class'] = 'form-control'
            self.fields['request_desc'].widget.attrs['class'] = 'form-control'
            self.fields['request_desc'].widget.attrs['id'] = 'Description'


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
    email_boss = forms.EmailField(max_length=200, required=False, widget=forms.HiddenInput)
    email_ib = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)
    user_boss = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)
    full_status_request = forms.CharField(max_length=200, required=False, initial="Ожидание согласования руководителя",
                                          widget=forms.HiddenInput)
    change_date = forms.CharField(max_length=200, widget=forms.HiddenInput, required=False)

    class Meta:
        model = ApproveList
        fields = '__all__'
        widgets = {'': forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['email_boss'].widget = forms.HiddenInput()
            self.fields['approve_status_boss'].widget = forms.HiddenInput()
            self.fields['approve_status_ib'].widget = forms.HiddenInput()
            self.fields['full_status_request'].widget = forms.HiddenInput()
            self.fields['ib_spec'].widget = forms.HiddenInput()
            self.fields[field].widget.attrs['class'] = 'form-control'
            # self.fields['email_boss'].widget.attrs['class'] = 'form-control'
            # self.fields['email_boss'].widget.attrs['readonly'] = False
            # self.fields['email_ib'].widget.attrs['readonly'] = True


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('address',)


class AccepterForm(forms.ModelForm):
    Cool_Story = forms.MultipleChoiceField(choices=SERVICES,
                                           widget=forms.CheckboxSelectMultiple(), required=False)

    # Access_ID = forms.ChoiceField(required=False, initial=Access.objects.get(id=40))
    Accepter_FIO = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput, initial="Access_ID")
    # Accepted_Service = forms.ChoiceField( required=False,initial=Service.objects.get(id=1))
    Email_Accepter = forms.EmailField(required=False, widget=forms.HiddenInput, initial="Access_ID@mail.rus")
    Accepter_Status = forms.CharField(max_length=100, widget=forms.HiddenInput, required=False, initial="Ожидание")

    class Meta:
        model = List_of_Accept
        fields = '__all__'
        widgets = {
            'Acceter_FIO': forms.HiddenInput,
            'Access_ID': forms.HiddenInput,
            'Accepted_Service': forms.HiddenInput,
            'Email_Accepter': forms.HiddenInput,
            'Accepter_Status': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        # self.fields['Accepted_Service'].widget = forms.CheckboxSelectMultiple()
        # self.fields['Cool_Story'].widget.attrs['required'] = 'True'


class Additional_Service(forms.Form):
    rulechoicer = forms.ChoiceField(choices=SERVICES, required=False)


class File_Deps_Form(forms.Form):
    FILE_DEPS = (
        (1, "Выберите корневую папку"),
        ("Департамент анализа эффективности перевозок", "Департамент анализа эффективности перевозок"),
        ("Департамент безопасности", "Департамент безопасности"),
        ("Департамент вагонного хозяйства", "Департамент вагонного хозяйства"),
        (4, "Департамент взаиморасчетов"),
        (5, "Департамент внешних связей"),
        (6, "Департамент информационных технологий"),
        (7, "Департамент корпоративного управления"),
        (8, "Департамент по управлению персоналом"),
        (9, "Департамент правового сопровождения"),
        (10, "Департамент продаж"),
        (11, "Департамент стратегического маркетинга"),
        (12, "Департамент стратегического развития"),
        (13, "Департамент транспортно-экспедиционного обслуживания"),
        (14, "Департамент финансов и казначейства"),
        (15, "Департамент экономики и финансов")

    )
    selector_deps = forms.ChoiceField(choices=FILE_DEPS, required=False, label='Выбор корневой папки',
                                      widget=forms.CheckboxSelectMultiple())
