from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.TextField('first_name')
    last_name = models.TextField('last_name')
    username = models.TextField('username')
    email = models.EmailField('email')
    role = models.CharField('role',max_length = 100,default="user")
    password = models.CharField('password',max_length=100)
    phone = models.CharField("phone",max_length=100,default="+2348109545948")
    age = models.IntegerField('age',default=0)
    status = models.CharField('status',max_length=100,default="active")
    class Meta:
        db_table = 'Users'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'





