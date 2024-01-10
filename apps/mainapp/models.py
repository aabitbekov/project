# YourApp/models.py
from django.db import models

class Signal(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    timestamp = models.DateTimeField(
        verbose_name="Дата и время",
        blank=False,
        null=False
        )
    ip_src = models.GenericIPAddressField(
        verbose_name="SRC IP",
        blank=True,
        null=True
        )
    ip_dst = models.GenericIPAddressField(
        verbose_name="DST IP",
        blank=True, 
        null=True
        )
    user = models.CharField(("Источник"), max_length=50)
    message_text = models.TextField(verbose_name="Сообщение",)

    class Meta:
        verbose_name = 'Сигнал'
        verbose_name_plural = 'Сигналы'

    def __str__(self):
        ip = self.ip_dst
        znak = '⭕'
        if self.ip_src:
            ip = self.ip_src
            znak = '❌'
        return f"Incident: {znak} {ip} "
    

class Incident(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    timestamp = models.DateTimeField(
        verbose_name="Дата и время",
        blank=False,
        null=False
        )
    ip = models.GenericIPAddressField(
        verbose_name="IP-адрес",
        blank=True, 
        null=True   
        )
    matching_count = models.IntegerField(verbose_name="Сигналы")
    signals = models.ManyToManyField(Signal, verbose_name="Сигналы")


    class Meta:
        verbose_name = 'Инцидент'
        verbose_name_plural = 'Инциденты'












