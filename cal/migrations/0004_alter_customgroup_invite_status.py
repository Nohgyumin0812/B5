# Generated by Django 4.0.3 on 2022-06-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_customgroup_invite_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='invite_status',
            field=models.CharField(default=1, max_length=50),
        ),
    ]
