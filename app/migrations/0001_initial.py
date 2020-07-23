# Generated by Django 2.1.9 on 2020-07-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuData',
            fields=[
                ('Add_Date', models.DateField(auto_now=True)),
                ('Item_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Item_Category', models.CharField(max_length=20)),
                ('Item_Name', models.CharField(max_length=50)),
                ('Item_Price', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'MenuData',
            },
        ),
    ]