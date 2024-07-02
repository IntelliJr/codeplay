# Generated by Django 5.0.1 on 2024-03-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_remove_usertolang_language_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('date_joined', models.DateField(blank=True, null=True)),
                ('education_level', models.TextField(blank=True, null=True)),
                ('problems_attempted', models.IntegerField(blank=True, null=True)),
                ('problems_solved', models.IntegerField(blank=True, null=True)),
                ('exp_points', models.IntegerField(blank=True, null=True)),
                ('global_rank', models.IntegerField(blank=True, null=True)),
                ('is_mentor', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
    ]
