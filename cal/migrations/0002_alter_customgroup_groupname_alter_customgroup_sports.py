# Generated by Django 4.0.3 on 2022-06-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='groupname',
            field=models.CharField(max_length=200, null=True, unique=True, verbose_name='groupname'),
        ),
        migrations.AlterField(
            model_name='customgroup',
            name='sports',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
