from django import forms


class PlaceBidForm(forms.Form):
    amount = forms.DecimalField(min_value=0)
