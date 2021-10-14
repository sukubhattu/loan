from django import forms
from .constants import LOAN_TYPE


class LoanOrderForm(forms.Form):
    loan_amount = forms.FloatField(
        label='Loan Amount', widget=forms.TextInput(attrs={'placeholder': 'Your Loan Amount'})
    )
    loan_term = forms.IntegerField(
        label='Loan Term in Years', widget=forms.TextInput(attrs={'placeholder': 'Your Loan Term in Years'})
    )
    loan_type = forms.ChoiceField(label='Loan Type', choices=LOAN_TYPE)

    def clean(self):
        cleaned_data = super().clean()
        loan_term_value = cleaned_data.get('loan_term')
        loan_amount_value = cleaned_data.get('loan_amount')
        if loan_amount_value < 1000000:
            raise forms.ValidationError({'loan_amount': 'Loan amount should be greater than 1 Million'})
        if loan_term_value <= 0:
            raise forms.ValidationError({'loan_term': 'Loan term cannot be zero or less'})
        elif loan_term_value > 40:
            raise forms.ValidationError({'loan_term': 'Loan term cannot be more than 40 years'})
