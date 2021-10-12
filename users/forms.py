from django import forms
from django.db import models
from django.db.models.expressions import F
from django.forms.fields import DateField
from .constants import GENDER
from django.contrib.admin.widgets import AdminDateWidget

from django.forms.widgets import NumberInput

import re


def is_valid_phone_number(number):
    if len(number) < 10 or len(number) > 10:
        return False
    pattern = re.compile("9?[7-9][0-9]{9}")
    return pattern.match(number)


class UserProfileForm(forms.Form):
    first_name = forms.CharField(
        label='First Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your First Name'})
    )
    last_name = forms.CharField(
        label='Last Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Last Name'})
    )
    address = forms.CharField(
        label='Address', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Address'})
    )
    gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=GENDER))
    date_of_birth = forms.DateTimeField(
        required=False, label="Date", widget=NumberInput(attrs={'type': 'date', 'id': 'dob'})
    )
    contact_number = forms.IntegerField(
        label='Contact Number', widget=forms.TextInput(attrs={'placeholder': 'Your Contact Number'})
    )
    loan_amount = forms.FloatField(
        label='Loan Amount', widget=forms.TextInput(attrs={'placeholder': 'Your Loan Amount'})
    )
    loan_term = forms.IntegerField(
        label='Loan Term in Years', widget=forms.TextInput(attrs={'placeholder': 'Your Loan Term in Years'})
    )
    installment_amount = forms.FloatField(
        label='Installment Amount',
        widget=forms.TextInput(attrs={'placeholder': 'Your Installment Amount'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        contact_number_value = cleaned_data.get('contact_number')
        loan_term_value = cleaned_data.get('loan_term')
        loan_amount_value = cleaned_data.get('loan_amount')
        installment_amount_value = cleaned_data.get('installment_amount')
        is_valid_contact = is_valid_phone_number(str(contact_number_value))
        if not is_valid_contact:
            raise forms.ValidationError({'contact_number': 'Enter valid contact number'})
        if loan_amount_value < 1000000:
            raise forms.ValidationError({'loan_amount': 'Loan amount should be greater than 1 Million'})
        if loan_term_value <= 0:
            raise forms.ValidationError({'loan_term': 'Loan term cannot be zero or less'})
        elif loan_term_value > 40:
            raise forms.ValidationError({'loan_term': 'Loan term cannot be more than 40 years'})
        if installment_amount_value > loan_amount_value:
            raise forms.ValidationError(
                {'installment_amount': 'Installment amount cannot be greater than loan amount'}
            )
