# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('payment', models.CharField(max_length=255)),
                ('ctype', models.CharField(default=b'hours', max_length=5, choices=[(b'total', b'total'), (b'hours', b'hours')])),
                ('lang', models.CharField(default=b'es', max_length=2, choices=[(b'es', b'es'), (b'en', b'en')])),
                ('locale', models.CharField(max_length=31)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invoice',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 27, 11, 9, 15, 61969, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(to='invoices.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='dateformat',
            field=models.CharField(default=b'%d de %B de %Y', max_length=31),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='expirydate',
            field=models.PositiveSmallIntegerField(default=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fee',
            name='fee',
            field=models.FloatField(default=35.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='num',
            field=models.PositiveIntegerField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='year',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Year',
        ),
        migrations.AlterField(
            model_name='project',
            name='tax',
            field=models.FloatField(default=21.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='taxname',
            field=models.CharField(default=b'IVA (21%)', max_length=31),
            preserve_default=True,
        ),
    ]
