# Generated by Django 4.0.3 on 2022-05-18 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0006_alter_customgroup_date_alter_customgroup_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customgroup',
            name='date',
        ),
    ]
