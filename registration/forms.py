from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from registration.models import User, IDPinGenerate


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=8, label="ID Pin")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'contact_number', 'email', 'address',
                  'password1', 'password2', 'document', 'date_of_birth']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'date_of_birth': DatePickerInput(format='%d/%m/%Y'),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['contact_number'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['document'].required = True
        self.fields['date_of_birth'].required = True

    def clean(self):
        super(SignUpForm, self).clean()
        id_pin = self.cleaned_data['username']
        if not IDPinGenerate.objects.filter(created_user__isnull=True, id_pin=id_pin).exists():
            self._errors['username'] = self.error_class(['Incorrect ID Pin.'])
        return self.cleaned_data
