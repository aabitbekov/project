# Generated by Django 4.2 on 2024-01-11 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(verbose_name='Дата и время')),
                ('ip_src', models.GenericIPAddressField(blank=True, null=True, verbose_name='SRC IP')),
                ('ip_dst', models.GenericIPAddressField(blank=True, null=True, verbose_name='DST IP')),
                ('uid', models.IntegerField()),
                ('user', models.IntegerField(verbose_name='Источник')),
                ('message_text', models.TextField(verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Сигнал',
                'verbose_name_plural': 'Сигналы',
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(verbose_name='Дата и время')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP-адрес')),
                ('matching_count', models.IntegerField(verbose_name='Сигналы')),
                ('signals', models.ManyToManyField(to='mainapp.signal', verbose_name='Сигналы')),
            ],
            options={
                'verbose_name': 'Инцидент',
                'verbose_name_plural': 'Инциденты',
            },
        ),
    ]
