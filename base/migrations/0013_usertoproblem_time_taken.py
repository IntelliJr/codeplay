# Generated by Django 5.0.1 on 2024-03-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_pendingproblem'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoproblem',
            name='time_taken',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
