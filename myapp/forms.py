from django import forms
from.models import product




class editproductform(forms.ModelForm):
    class Meta:
        model=product
        fields=['medicinename','price','quantity','company','type','image']


