# Generated by Django 3.2.7 on 2021-12-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='No_EMAIL', max_length=254, unique=True),
        ),
    ]