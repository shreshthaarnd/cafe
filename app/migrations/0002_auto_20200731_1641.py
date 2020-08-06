# Generated by Django 2.1.9 on 2020-07-31 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategoryData',
            fields=[
                ('Add_Date', models.DateTimeField(auto_now=True)),
                ('Category_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Category_Name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'MenuCategoryData',
            },
        ),
        migrations.AlterField(
            model_name='menudata',
            name='Add_Date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]