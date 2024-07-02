# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            date_joined = timezone.now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

# # class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     username = models.TextField(blank=True, null=True)
#     first_name = models.TextField(blank=True, null=True)
#     last_name = models.TextField(blank=True, null=True)
#     date_joined = models.DateField(blank=True, null=True)
#     education_level = models.TextField(blank=True, null=True)
#     problems_attempted = models.IntegerField(blank=True, null=True)
#     problems_solved = models.IntegerField(blank=True, null=True)
#     exp_points = models.IntegerField(blank=True, null=True)
#     global_rank = models.IntegerField(blank=True, null=True)
#     is_mentor = models.BooleanField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'user'
    
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField(blank=True, null=True, unique=True)
    password = models.TextField(max_length=128, verbose_name='password')
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True, auto_now_add=True)
    education_level = models.TextField(blank=True, null=True)
    problems_attempted = models.IntegerField(blank=True, null=True)
    problems_solved = models.IntegerField(blank=True, null=True)
    exp_points = models.IntegerField(blank=True, null=True)
    global_rank = models.IntegerField(blank=True, null=True)
    is_mentor = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    class Meta:
        managed = True
        db_table = 'user'

class Chatroom(models.Model):
    chat_id = models.AutoField(primary_key=True)
    mentee = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    mentor = models.ForeignKey(User, models.DO_NOTHING, related_name='chatroom_mentor_set', blank=True, null=True)
    msg_id = models.IntegerField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    origin_of_msg = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chatroom'


class CodingLanguage(models.Model):
    language_id = models.TextField(primary_key=True)
    language_name = models.TextField()

    def __str__(self):
        return self.language_name

    class Meta:
        managed = True
        db_table = 'coding_language'

class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    difficulty = models.TextField(blank=True, null=True)
    test_cases = models.TextField(blank=True, null=True)
    exp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'problem'




class Topics(models.Model):
    topics = models.TextField(null = True, blank = True)

class ProblemToTopic(models.Model):
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    topic = models.ForeignKey(Topics, models.DO_NOTHING)

    
class PendingProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor_assigned = models.BooleanField(default=False)
    
class ProblemToLang(models.Model):
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    language = models.ForeignKey(CodingLanguage, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'problem_to_lang'     

class UserToLang(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    language = models.ForeignKey(CodingLanguage, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_to_lang'


class UserToProblem(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    solved = models.BooleanField()
    time_taken = models.IntegerField(null = True, blank= True)
    #Added new FK field: language_id so that we can handle multiple languages having the same problem_id
    language = models.ForeignKey(CodingLanguage, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'user_to_problem'

class MentorAvailability(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    is_available = models.BooleanField(default=False)
    
