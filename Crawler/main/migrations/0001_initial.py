# Generated by Django 4.1.4 on 2023-01-04 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=255)),
                ('numberBedrooms', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('img', models.CharField(max_length=255)),
            ],
        ),
    ]
