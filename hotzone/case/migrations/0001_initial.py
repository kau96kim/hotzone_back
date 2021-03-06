# Generated by Django 3.1.3 on 2020-11-03 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('virus', '0001_initial'),
        ('location', '0002_auto_20201103_0809'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date_confirmed', models.DateField()),
                ('local_or_imported', models.CharField(choices=[('Local', 'Local'), ('Imported', 'Imported')], default='Local', max_length=10)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('virus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virus.virus')),
            ],
        ),
        migrations.CreateModel(
            name='CaseLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('category', models.CharField(choices=[('Residence', 'Residence'), ('Workplace', 'Workplace'), ('Visit', 'Visit')], default='Visit', max_length=10)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.case')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
            ],
        ),
    ]
