# Generated by Django 2.2.5 on 2022-04-05 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id_num', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('passWord', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=10)),
                ('tel', models.CharField(max_length=10)),
                ('emailAddr', models.EmailField(max_length=40)),
            ],
        ),
    ]
