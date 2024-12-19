# Generated by Django 5.1.4 on 2024-12-19 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutismFormInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a1_score', models.IntegerField()),
                ('a2_score', models.IntegerField()),
                ('a3_score', models.IntegerField()),
                ('a4_score', models.IntegerField()),
                ('a5_score', models.IntegerField()),
                ('a6_score', models.IntegerField()),
                ('a7_score', models.IntegerField()),
                ('a8_score', models.IntegerField()),
                ('a9_score', models.IntegerField()),
                ('a10_score', models.IntegerField()),
                ('total_score', models.IntegerField()),
                ('age_desc', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('ethnicity', models.CharField(max_length=100)),
                ('jundice', models.CharField(max_length=5)),
                ('austim', models.CharField(max_length=5)),
                ('country_of_res', models.CharField(max_length=100)),
                ('used_app_before', models.CharField(max_length=5)),
                ('relation', models.CharField(max_length=100)),
                ('asd', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
