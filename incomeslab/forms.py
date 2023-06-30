from django import forms

from registration.models import IDPinGenerate


class IDPinGenerateForm(forms.ModelForm):
    class Meta:
        model = IDPinGenerate
        fields = ['share_no', 'share_price']
