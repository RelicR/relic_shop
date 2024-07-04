import django.core.validators
from django.db import models
from django.utils import timezone


class CityModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class StreetModel(models.Model):
    name = models.CharField(max_length=63, verbose_name='Название')
    city = models.CharField(max_length=50, verbose_name='Город')
    idCity = models.ForeignKey(CityModel, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        unique_together = ('name', 'city')

    def __str__(self):
        return self.name


class ShopModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=63, verbose_name='Улица')
    building = models.CharField(max_length=7,
                                verbose_name='Дом',
                                validators=[django.core.validators.RegexValidator(regex=r'^\d+[а-яА-Я]?(\/\d+[а-яА-Я]?)?$')])
    start = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Время открытия', default=timezone.localtime().time().min)
    end = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Время закрытия', default=timezone.localtime().time().max)
    idCity = models.ForeignKey(CityModel, on_delete=models.CASCADE, default=0)
    idStreet = models.ForeignKey(StreetModel, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        unique_together = ('name', 'city', 'street', 'building')

    def __str__(self):
        return self.name
