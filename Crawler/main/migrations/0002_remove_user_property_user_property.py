# Generated by Django 4.1.4 on 2023-01-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='property',
        ),
        migrations.AddField(
            model_name='user',
            name='property',
            field=models.ManyToManyField(blank=True, null=True, to='main.property'),
        ),
    ]
