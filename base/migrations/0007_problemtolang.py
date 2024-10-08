# Generated by Django 5.0.1 on 2024-03-15 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemToLang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.codinglanguage')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.problem')),
            ],
            options={
                'db_table': 'problem_to_lang',
                'managed': True,
            },
        ),
    ]
