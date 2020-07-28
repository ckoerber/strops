# Generated by Django 3.1a1 on 2020-07-07 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import strops.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('references', '0002_auto_20200707_0920'),
        ('operators', '0002_auto_20200707_0959'),
        ('parameters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpansionOrder',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('power', models.IntegerField(help_text='The power of the expansion paramter in given relation.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpansionParameter',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.CharField(help_text='Name of the parameter scheme.', max_length=256)),
                ('symbol', strops.utils.fields.SympyField(encoder='symbol', help_text='Symbol representing this parameter.')),
                ('description', models.TextField(help_text='What does this parameter describe, which assumptions are made?')),
                ('natural_size', models.DecimalField(blank=True, decimal_places=4, help_text="Estimate of parameter size under 'regular' conditions.", max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpansionScheme',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('name', models.CharField(help_text='Name of the expansion scheme.', max_length=256)),
                ('source_scale', models.CharField(choices=[('quark', 'Quark'), ('nucleon', 'Nucleon'), ('nucleon-nr', 'Non-relativistic nuclear scale')], help_text='The source scale of the expansion.', max_length=256)),
                ('target_scale', models.CharField(choices=[('quark', 'Quark'), ('nucleon', 'Nucleon'), ('nucleon-nr', 'Non-relativistic nuclear scale')], help_text='The target scale of the expansion.', max_length=256)),
                ('references', models.ManyToManyField(help_text='Publications specifying the operator relationship.', to='references.Publication')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperatorRelation',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('factor', strops.utils.fields.SympyField(encoder='expression', help_text="Factor associated with the propagation of scales. E.g., 'source -> factor * target' at 'order'.")),
                ('order', models.ManyToManyField(help_text='Information allowing to order different operators by their relevance. E.g., chiral power counting scheme.', through='schemes.ExpansionOrder', to='schemes.ExpansionParameter')),
                ('parameters', models.ManyToManyField(help_text='Non-expansion paramters present in the factor.', to='parameters.Parameter')),
                ('references', models.ManyToManyField(help_text='Publications specifying the operator relationship.', to='references.Publication')),
                ('scheme', models.ForeignKey(help_text="Key for grouping different schemes to form a complete representation (e.g., if an expansion scheme is workout over several publications). Relationships with the same tag should share the same 'order' keys to allow sorting them by relevance. ", on_delete=django.db.models.deletion.CASCADE, to='schemes.expansionscheme')),
                ('source', models.ForeignKey(help_text='More fundamental operator as a source for the propagation of scales.', on_delete=django.db.models.deletion.CASCADE, related_name='source_for', to='operators.operator')),
                ('target', models.ForeignKey(help_text='Operator as a source for the propagation of scales.', on_delete=django.db.models.deletion.CASCADE, related_name='target_of', to='operators.operator')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='expansionparameter',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schemes.expansionscheme'),
        ),
        migrations.AddField(
            model_name='expansionparameter',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expansionorder',
            name='parameter',
            field=models.ForeignKey(help_text='The expansion parameter for relating different operators.', on_delete=django.db.models.deletion.CASCADE, to='schemes.expansionparameter'),
        ),
        migrations.AddField(
            model_name='expansionorder',
            name='relation',
            field=models.ForeignKey(help_text='The relation between operators at different scales.', on_delete=django.db.models.deletion.CASCADE, to='schemes.operatorrelation'),
        ),
        migrations.AddField(
            model_name='expansionorder',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='expansionparameter',
            constraint=models.UniqueConstraint(fields=('name', 'scheme'), name='Unique name and scheme'),
        ),
        migrations.AddConstraint(
            model_name='expansionparameter',
            constraint=models.UniqueConstraint(fields=('scheme', 'symbol'), name='Unique symbol and scheme'),
        ),
    ]