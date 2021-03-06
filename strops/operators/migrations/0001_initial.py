# Generated by Django 3.1a1 on 2020-07-07 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import strops.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.CharField(help_text='Name of the operator which can be used for searches.', max_length=256, unique=True)),
                ('scale', models.CharField(choices=[('quark', 'Quark'), ('nucleon', 'Nucleon'), ('nucleon-nr', 'Non-relativistic nuclear scale')], help_text='Scale at which this degree of freedom interacts.', max_length=256)),
                ('charge', models.IntegerField(choices=[(1, '+'), (-1, '-')], help_text='Charge transformation behavior of operator.')),
                ('parity', models.IntegerField(choices=[(1, '+'), (-1, '-')], help_text='Parity transformation behavior of operator.')),
                ('time', models.IntegerField(choices=[(1, '+'), (-1, '-')], help_text='Time transformation behavior of operator.')),
                ('lorentz', models.CharField(choices=[('s', 'Scalar'), ('v', 'Vector'), ('ps', 'Pseudo Scalar'), ('pv', 'Pseudo Vector'), ('t', 'Tensor'), ('pt', 'Pseudo Tensor')], help_text='How does this operator behave under Lorentz transformations?', max_length=2)),
                ('details', models.JSONField(blank=True, help_text='Further optional information to specify the operator.', null=True)),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('scale', models.CharField(choices=[('quark', 'Quark'), ('nucleon', 'Nucleon'), ('nucleon-nr', 'Non-relativistic nuclear scale')], help_text='Scale at which this degree of freedom interacts.', max_length=256)),
                ('kind', models.CharField(choices=[('up', 'up'), ('down', 'down'), ('strange', 'strange'), ('proton', 'proton'), ('neutron', 'neutron'), ('pion', 'pion'), ('proton', 'proton'), ('neutron', 'neutron'), ('pion', 'pion')], help_text="Descriptive name like 'up' for the quark scale or 'proton' for the nucleon scale.", max_length=256)),
                ('conjugated', models.BooleanField(default=False, help_text='Is field conjugated (dagger, bar) or not.')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('scale', 'kind', 'conjugated')},
            },
        ),
        migrations.CreateModel(
            name='TwoFieldOperator',
            fields=[
                ('operator_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='operators.operator')),
                ('matrix1', strops.utils.fields.SympyField(encoder='non-commutative-expression', help_text='Term representing the operator. For example $\\gamma_5$', unique=True)),
                ('field1', models.ForeignKey(help_text='Conjugated field present on the left of the operator expression (e.g., Bar(u)).', on_delete=django.db.models.deletion.CASCADE, related_name='operators_21', to='operators.field')),
                ('field2', models.ForeignKey(help_text='Field present on the right of the operator expression (e.g., d).', on_delete=django.db.models.deletion.CASCADE, related_name='operators_22', to='operators.field')),
            ],
            options={
                'abstract': False,
            },
            bases=('operators.operator',),
        ),
    ]
