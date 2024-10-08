# Generated by Django 5.0.1 on 2024-03-17 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_mentoravailability'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor_assigned', models.BooleanField(default=False)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.problem')),
            ],
        ),
    ]
