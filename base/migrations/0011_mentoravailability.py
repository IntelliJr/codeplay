# Generated by Django 5.0.1 on 2024-03-16 12:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_user_password_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorAvailability',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_available', models.BooleanField(default=False)),
            ],
        ),
    ]
