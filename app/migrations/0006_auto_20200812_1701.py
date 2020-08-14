# Generated by Django 2.1.9 on 2020-08-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200808_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='menudata',
            name='Status',
            field=models.CharField(default='Active', max_length=10),
        ),
        migrations.AddField(
            model_name='paymentdata',
            name='PayMode',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentdata',
            name='Receipt_Number',
            field=models.CharField(default='NA if Cash', max_length=50),
        ),
    ]
