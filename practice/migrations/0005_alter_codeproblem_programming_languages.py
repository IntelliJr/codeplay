# Generated by Django 5.0.1 on 2024-03-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0004_alter_codeproblem_programming_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeproblem',
            name='programming_languages',
            field=models.CharField(choices=[('JAVA', 'Java'), ('PYTHON', 'Python'), ('C++', 'Cpp')], default='', max_length=20),
        ),
    ]
