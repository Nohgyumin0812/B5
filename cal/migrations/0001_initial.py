# Generated by Django 4.0.3 on 2022-06-10 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=200, unique=True, verbose_name='groupname')),
                ('sports', models.CharField(default='', max_length=50)),
                ('friendname', models.CharField(blank=True, default='', max_length=50)),
                ('location', models.CharField(blank=True, default='', max_length=50)),
                ('location_code', models.CharField(blank=True, default='', max_length=50)),
                ('x', models.CharField(blank=True, default='', max_length=50)),
                ('y', models.CharField(blank=True, default='', max_length=50)),
                ('dateFirst', models.CharField(blank=True, default='', max_length=50)),
                ('sportFirst', models.CharField(blank=True, default='', max_length=50)),
                ('members', models.ManyToManyField(blank=True, default='', related_name='members', to=settings.AUTH_USER_MODEL, verbose_name='members')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InviteGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_user', models.CharField(blank=True, default='', max_length=50)),
                ('group', models.CharField(blank=True, default='', max_length=50)),
                ('invite_status', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DayGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myDates', models.CharField(default='', max_length=100)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cal.customgroup', verbose_name='group')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
    ]
