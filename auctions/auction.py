from django import forms


class PlaceBidForm(forms.Form):
    amount = forms.DecimalField(min_value=0)


class CreateAuctionForm(forms.Form):
    item = forms.CharField(
        label="Item:", widget=forms.TextInput(attrs={"list": "items-list"})
    )
    price = forms.DecimalField(max_digits=6, decimal_places=2)


class CreateItemForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=30)
    description = forms.CharField(label="Description:", max_length=120)
