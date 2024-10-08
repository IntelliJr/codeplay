# Generated by Django 5.0.1 on 2024-03-19 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_usertoproblem_time_taken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='ProblemToTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.problem')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.topics')),
            ],
        ),
    ]
