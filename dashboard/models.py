from django.db import models


class Passwords(models.Model):
    user_id = models.IntegerField('user_id')
    name = models.CharField('name',max_length=150)
    app_name = models.CharField('app_name',max_length=150)
    generated_password = models.CharField('generated_password',max_length=200)
    password_length = models.IntegerField('password_length')

    class Meta:
        db_table = "passwords"
        managed = True 
    