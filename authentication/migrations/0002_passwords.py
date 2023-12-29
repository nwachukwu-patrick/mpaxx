# Generated by Django 5.0 on 2023-12-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('app_name', models.CharField(max_length=150, verbose_name='app_name')),
                ('generated_password', models.CharField(max_length=200, verbose_name='generated_password')),
                ('password_length', models.IntegerField(verbose_name='password_lenght')),
            ],
            options={
                'db_table': 'passwords',
                'managed': True,
            },
        ),
    ]