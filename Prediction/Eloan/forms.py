from django import forms

class LoanPredictionForm(forms.Form):
    no_of_dependents = forms.IntegerField(min_value=0, label='Number of Dependents')
    income_annum = forms.FloatField(min_value=0, label='Annual Income')
    loan_amount = forms.FloatField(min_value=0, label='Loan Amount')
    loan_term = forms.FloatField(min_value=0, label='Loan Term (Years)')
    cibil_score = forms.FloatField(min_value=300, max_value=900, label='CIBIL Score')
    residential_assets_value = forms.FloatField(min_value=0, label='Residential Assets Value')
    luxury_assets_value = forms.FloatField(min_value=0, label='Luxury Assets Value')
    bank_asset_value = forms.FloatField(min_value=0, label='Bank Asset Value')
    
    EDUCATION_CHOICES = [
        ('Graduate', 'Graduate'),
        ('Not Graduate', 'Not Graduate'),
    ]
    education = forms.ChoiceField(choices=EDUCATION_CHOICES, label='Education')

    SELF_EMPLOYED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    self_employed = forms.ChoiceField(choices=SELF_EMPLOYED_CHOICES, label='Self Employed')
