# Generated by Django 3.1rc1 on 2020-07-27 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0001_initial'),
        ('schemes', '0002_expansionscheme_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expansionparameter',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expansion_parameters', to='schemes.expansionscheme'),
        ),
        migrations.AlterField(
            model_name='operatorrelation',
            name='parameters',
            field=models.ManyToManyField(blank=True, help_text='Non-expansion paramters present in the factor.', to='parameters.Parameter'),
        ),
        migrations.AlterField(
            model_name='operatorrelation',
            name='scheme',
            field=models.ForeignKey(help_text="Key for grouping different schemes to form a complete representation (e.g., if an expansion scheme is workout over several publications). Relationships with the same tag should share the same 'order' keys to allow sorting them by relevance. ", on_delete=django.db.models.deletion.CASCADE, related_name='relations', to='schemes.expansionscheme'),
        ),
    ]
