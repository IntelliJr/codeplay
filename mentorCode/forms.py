from django import forms
from .models import CodingLanguage  # Import your CodingLanguage model

# Assuming simple difficulty choices
DIFFICULTY_CHOICES = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
)

TOPIC_CHOICES = (
    ('select_topic', 'Select Topic...'),
    ('for_loops', 'For Loops'),
    ('while_loops', 'While Loops'),
    ('conditional_statements', 'Conditional Statements'),
    ('1d_arrays', '1D Arrays'),
    ('dictionaries', 'Dictionaries'),
    ('recursion', 'Recursion'),
)
class MenteeProblemSearchForm(forms.Form):
    language = forms.ModelChoiceField(queryset=CodingLanguage.objects.all(), label="Coding Language")
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES)
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, required=False, label="Topic (optional)") 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].label_from_instance = lambda obj: obj.language_name 

class MentorRefresh(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       