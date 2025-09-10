from django import forms
from .models import Rate, FxConfig

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ["code", "rate_per_base"]

class BatchForm(forms.Form):
    rates_json = forms.CharField(
        widget=forms.Textarea,
    )

class ConvertForm(forms.Form):
    source = forms.ChoiceField(label="De", choices=[])
    target = forms.ChoiceField(label="Para", choices=[])
    amount = forms.DecimalField(min_value=0, decimal_places=6, max_digits=16, label="Amount")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        codes = list(Rate.objects.order_by('code').values_list('code', flat=True))
        base = FxConfig.get_base()
        if base not in codes:
            codes = [base] + codes
        choices = [(c, c) for c in codes]
        self.fields["source"].choices = choices
        self.fields["target"].choices = choices
 