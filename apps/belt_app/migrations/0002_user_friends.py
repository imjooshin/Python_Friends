# Generated by Django 2.0.7 on 2018-07-27 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='_user_friends_+', to='belt_app.User'),
        ),
    ]