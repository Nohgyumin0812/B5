# Generated by Django 4.0.3 on 2022-06-11 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0005_invitegroupgroup_owner_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='mixCustomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(blank=True, default='', max_length=50)),
                ('owner', models.CharField(blank=True, default='', max_length=50)),
                ('members', models.CharField(blank=True, default='', max_length=50)),
                ('sports', models.CharField(blank=True, default='', max_length=50)),
                ('friendname', models.CharField(blank=True, default='', max_length=50)),
                ('location', models.CharField(blank=True, default='', max_length=50)),
                ('location_code', models.CharField(blank=True, default='', max_length=50)),
                ('x', models.CharField(blank=True, default='', max_length=50)),
                ('y', models.CharField(blank=True, default='', max_length=50)),
                ('dateFirst', models.CharField(blank=True, default='', max_length=50)),
                ('sportFirst', models.CharField(blank=True, default='', max_length=50)),
                ('invite_status', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
    ]
