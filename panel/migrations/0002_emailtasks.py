# Generated by Django 2.2.6 on 2020-02-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.CharField(default='2000-01-01T00:00:00', max_length=20)),
                ('to', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
    ]
