# Generated by Django 5.0 on 2023-12-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passwords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='user_id')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('app_name', models.CharField(max_length=150, verbose_name='app_name')),
                ('generated_password', models.CharField(max_length=200, verbose_name='generated_password')),
                ('password_length', models.IntegerField(verbose_name='password_length')),
            ],
            options={
                'db_table': 'passwords',
                'managed': True,
            },
        ),
    ]