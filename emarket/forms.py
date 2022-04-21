from django import forms
from products.models import Product


class ContactForm(forms.Form):
    """
    Contact form for customer support via email
    """
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size': '40', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)


class FilterForm(forms.Form):
    """
    Filter form from the home page.
    """
    fields_with_choices = [
        'os',
        'diagonal',
        'processor',
        'ram'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creating choices for every field in filter
        for field in self.fields_with_choices:
            self.fields[field].choices = Product.get_field_choices(field)

        # Fields in the filter are not required to be used
        for field in self.fields.keys():
            self.fields[field].required = False

        self.fields['min_price'].label = "Min price: " + str(Product.get_min_price()) + ' RUB'
        self.fields['max_price'].label = "Max price: " + str(Product.get_max_price()) + ' RUB'

    os = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    diagonal = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    processor = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    ram = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    memory_min = forms.IntegerField(
        initial=Product.get_min_memory,
        max_value=99999,
        min_value=0
    )
    memory_max = forms.IntegerField(
        initial=Product.get_max_memory,
        max_value=99999,
        min_value=0
    )
    min_price = forms.IntegerField(initial=Product.get_min_price,
                                   widget=forms.NumberInput(attrs={'type': 'range',
                                                                   'min': Product.get_min_price,
                                                                   'id': 'mprice',
                                                                   'max': Product.get_max_price,
                                                                   'oninput': 'printprice("mprice")'}))

    max_price = forms.IntegerField(initial=Product.get_max_price,
                                   widget=forms.NumberInput(attrs={'type': 'range',
                                                                   'min': Product.get_min_price,
                                                                   'id': 'maxprice',
                                                                   'max': Product.get_max_price,
                                                                   'oninput': 'printprice("maxprice")'}))

    search = forms.CharField(max_length=200, widget=forms.HiddenInput())
