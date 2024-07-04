from rest_framework import serializers
from . import models


class CityModelSerializer(serializers.ModelSerializer):
    city_list = serializers.SerializerMethodField()

    class Meta:
        model = models.CityModel
        fields = ['city_list', ]

    @staticmethod
    def get_city_list(obj):
        return [
            dict(id=x.id, city=x.name) for x in obj
        ] if hasattr(obj, '__iter__') else dict(id=obj.id, city=obj.name)


class StreetModelSerializer(serializers.ModelSerializer):
    street_list = serializers.SerializerMethodField()

    class Meta:
        model = models.StreetModel
        fields = ['street_list', ]

    @staticmethod
    def get_street_list(obj):
        return [
            dict(id=x.id, street=x.name, city=x.city) for x in obj
        ] if hasattr(obj, '__iter__') else dict(id=obj.id, street=obj.name, city=obj.city)


class ShopModelSerializer(serializers.ModelSerializer):
    shop_list = serializers.SerializerMethodField()

    class Meta:
        model = models.ShopModel
        fields = ['shop_list', ]

    @staticmethod
    def get_shop_list(obj):
        return [
            dict(id=x.id, shop=x.name, city=x.city, street=x.street) for x in obj
        ] if hasattr(obj, '__iter__') else dict(id=obj.id, shop=obj.name, city=obj.city, street=obj.street)
