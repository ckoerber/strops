# Generated by Django 3.1rc1 on 2020-07-29 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0003_auto_20200728_1849'),
        ('schemes', '0005_auto_20200729_0936'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='operatorrelation',
            unique_together={('source', 'target', 'scheme', 'factor')},
        ),
    ]