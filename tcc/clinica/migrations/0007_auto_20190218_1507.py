# Generated by Django 2.1.5 on 2019-02-18 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0006_medicamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='fabricante',
            field=models.CharField(max_length=100, verbose_name='Fabricante'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='nomeComercial',
            field=models.CharField(max_length=100, verbose_name='Nome Comercial'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='nomeGenerico',
            field=models.CharField(max_length=100, verbose_name='Nome Generico'),
        ),
    ]