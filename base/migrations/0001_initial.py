# Generated by Django 5.0.1 on 2024-03-15 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodingLanguage',
            fields=[
                ('language_id', models.TextField(primary_key=True, serialize=False)),
                ('language_name', models.TextField()),
            ],
            options={
                'db_table': 'coding_language',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problem_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('difficulty', models.TextField(blank=True, null=True)),
                ('test_cases', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'problem',
                'managed': True,
            },
        ),
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
        migrations.AddField(
            model_name='problem',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.user'),
        ),
        migrations.CreateModel(
            name='Chatroom',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('msg_id', models.IntegerField(blank=True, null=True)),
                ('msg', models.TextField(blank=True, null=True)),
                ('origin_of_msg', models.IntegerField(blank=True, null=True)),
                ('mentee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.user')),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='chatroom_mentor_set', to='base.user')),
            ],
            options={
                'db_table': 'chatroom',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserToLang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.codinglanguage')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.user')),
            ],
            options={
                'db_table': 'user_to_lang',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserToProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved', models.BooleanField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.user')),
            ],
            options={
                'db_table': 'user_to_problem',
                'managed': True,
            },
        ),
    ]
