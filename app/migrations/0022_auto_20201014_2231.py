# Generated by Django 3.1.1 on 2020-10-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_admindata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdata',
            name='Email',
            field=models.CharField(default='Not Availiable', max_length=50),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='Name',
            field=models.CharField(default='Not Availiable', max_length=100),
        ),
    ]
