# Generated by Django 4.0.3 on 2022-06-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0004_alter_customgroup_invite_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitegroupgroup',
            name='owner_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='customgroup',
            name='invite_status',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]