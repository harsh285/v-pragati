from django import forms

from registration.models import IDPinGenerate


class IDPinGenerateForm(forms.ModelForm):
    share_price_display = forms.CharField(max_length=256, required=False, disabled=True, label="Share Price")

    class Meta:
        model = IDPinGenerate
        fields = ['share_no', 'share_price_display']
