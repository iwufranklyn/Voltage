# Generated by Django 4.0.5 on 2022-06-09 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(default='a', max_length=20),
        ),
    ]
