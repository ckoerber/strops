# Generated by Django 3.1rc1 on 2020-07-29 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0002_auto_20200729_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value',
            field=models.JSONField(help_text='Value or descriptive information.', null=True),
        ),
    ]
