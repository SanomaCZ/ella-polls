# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ella_polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyvote',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, verbose_name='IP Address'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, verbose_name='IP Address'),
        ),
    ]
