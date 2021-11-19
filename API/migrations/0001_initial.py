# Generated by Django 3.2.7 on 2021-11-19 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('Dorm_id', models.AutoField(primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
                ('gender', models.CharField(max_length=25)),
                ('has_gym', models.BooleanField(default=False)),
                ('has_study_room', models.BooleanField(default=False)),
                ('has_game_room', models.BooleanField(default=False)),
                ('num_ppl', models.IntegerField()),
                ('max_ppl', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('Unit_id', models.AutoField(primary_key=True, serialize=False)),
                ('unit_name', models.CharField(default='Default', max_length=25)),
                ('num_ppl', models.IntegerField()),
                ('max_ppl', models.IntegerField()),
                ('has_kitchen', models.BooleanField(default=False)),
                ('has_laundry', models.BooleanField(default=False)),
                ('Dorm_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.dorm')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Bruh', max_length=25)),
                ('email', models.EmailField(default='No_EMAIL', max_length=254)),
                ('standing', models.CharField(max_length=25)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=15)),
                ('RA_id', models.IntegerField(null=True, unique=True)),
                ('Unit_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('Lease_id', models.AutoField(primary_key=True, serialize=False)),
                ('lease_type', models.CharField(default='Classic rippoff', max_length=25)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now=True, null=True)),
                ('User_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.user')),
            ],
        ),
    ]
