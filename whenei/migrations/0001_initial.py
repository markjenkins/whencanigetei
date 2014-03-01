# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EI_Economic_Place',
            fields=[
                ('code', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('province', models.CharField(max_length=2, choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('YT', 'Yukon'), ('ON', 'Ontario'), ('NL', 'Newfoundland and Labrador'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('SK', 'Saskatchewan'), ('QC', 'Quebec'), ('PE', 'Prince Edward Island'), ('NS', 'Nova Scotia'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rate_For_Place_And_Time',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('economic_place', models.ForeignKey(to='whenei.EI_Economic_Place', to_field='code')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('unemployment_rate', models.DecimalField(max_digits=4, decimal_places=1)),
            ],
            options={
                u'unique_together': set([('economic_place', 'start_date', 'end_date')]),
            },
            bases=(models.Model,),
        ),
    ]
