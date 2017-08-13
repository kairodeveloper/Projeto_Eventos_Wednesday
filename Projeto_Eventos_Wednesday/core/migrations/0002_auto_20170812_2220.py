# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 01:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='administrador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='atividades',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Atividade'),
        ),
        migrations.AddField(
            model_name='cupom',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Evento'),
        ),
        migrations.AddField(
            model_name='apoio',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apoios', to='core.Evento'),
        ),
        migrations.AddField(
            model_name='apoio',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Instituicao'),
        ),
    ]
