from django.db import models
from base.models import *

PROG_LANGUAGES = {
    "JAVA": "Java",
    "PYTHON": "Python",
    "CPP": "C++",
}

PROBLEM_DIFFICULTIES = {
    "EASY": "Easy",
    "MEDIUM": "Medium",
    "HARD": "Hard",
}

class CodeProblem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class ProblemDifficulty(models.TextChoices):
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"
    difficulty = models.CharField(max_length=6, choices=ProblemDifficulty, default="Easy")
    
    class ProgrammingLanguages(models.TextChoices):
        JAVA = "Java"
        PYTHON = "Python"
        C = "C"
        CPP = "C++"
    languages = models.CharField(max_length=20, choices=ProgrammingLanguages, default="")
    
    # topics = 
    experience_points = models.IntegerField()

    def __str__(self):
        return self.title
