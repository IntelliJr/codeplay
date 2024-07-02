from django import forms
from base.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_mentor = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.RadioSelect())
    EDUCATION_LEVEL_CHOICES = [
        ('SECONDARY_SCHOOL' , 'Secondary School'),
        ('YEAR_ONE_UNDERGRADUATE' , 'Year 1 Undergrad'),
        ('YEAR_TWO_UNDERGRADUATE' , 'Year 2 Undergrad'),
        ('YEAR_THREE_UNDERGRADUATE ' , 'Year 3 Undergrad'),
        ('YEAR_FOUR_UNDERGRADUATE ' , 'Year 4 Undergrad'),
        ('POSTGRADUATE' , 'Postgrad'),
        ('DOCTORATE' , 'Doctorate'),
        ('POSTDOCTORAL', 'Postdoc'),
        ('EMPLOYED' , 'Employed')
    ]
    education_level = forms.ChoiceField(label = 'Education Level', choices=EDUCATION_LEVEL_CHOICES)

    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'education_level', 'is_mentor', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'required': 'required'}),
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'last_name': forms.TextInput(attrs={'required': 'required'}),
            
            
        }


