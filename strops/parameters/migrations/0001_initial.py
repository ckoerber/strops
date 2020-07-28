# Generated by Django 3.1a1 on 2020-07-07 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import strops.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('references', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.CharField(help_text='Descriptive name of the variable', max_length=256)),
                ('symbol', strops.utils.fields.SympyField(encoder='expression', help_text='The mathematical symbol (Sympy syntax)')),
                ('value', models.JSONField(help_text='Value or descriptive information.')),
                ('reference', models.ForeignKey(help_text='Publication specifying the parameter.', on_delete=django.db.models.deletion.CASCADE, to='references.publication')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'reference')},
            },
        ),
    ]