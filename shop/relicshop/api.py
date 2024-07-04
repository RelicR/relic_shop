from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from django.utils import timezone
import overpy
import json


class GetCityList(APIView):
    @staticmethod
    def get(request):
        try:
            city = models.CityModel.objects.all()
            serialized_data = serializers.CityModelSerializer(city)
            return Response(serialized_data.data, status=200)
        except Exception:
            return Response(None, status=400)


class GetCityName(APIView):
    @staticmethod
    def get(request, city_id):
        try:
            city = models.CityModel.objects.get(id=city_id)
            serialized_data = serializers.CityModelSerializer(city)
            return Response(serialized_data.data, status=200)
        except Exception:
            return Response(None, status=400)


class SetCityStreets(APIView):
    @staticmethod
    def get(request, city_id):
        try:
            city_streets = set([x.name for x in models.StreetModel.objects.filter(idCity_id=city_id)])
            city_name = models.CityModel.objects.get(id=city_id).name
            result = overpy.Overpass().query(f"""[out:json][timeout:25];
area[name="{city_name}"]->.searchArea;
(
  node["addr:street"](area.searchArea);
  way["building" = "retail"](area.searchArea);
  relation["building" = "retail"](area.searchArea);
);
out body;
>;
out skel qt;""")
            temp_streets = set()
            for node in result.nodes:
                if len(node.tags) > 0:
                    temp_streets.add(node.tags['addr:street'])
            streets_to_add = [models.StreetModel(idCity_id=city_id, city=city_name, name=street) for street in set.difference(temp_streets, city_streets)]
            if len(streets_to_add) == 0:
                raise Exception
            del temp_streets, city_streets
            models.StreetModel.objects.bulk_create(streets_to_add)
            serialized_data = serializers.StreetModelSerializer(models.StreetModel.objects.filter(idCity_id=city_id))
            del streets_to_add, result
            return Response(serialized_data.data, status=200)
        except Exception:
            return Response(None, status=400)


class GetCityStreets(APIView):
    @staticmethod
    def get(request, city_id):
        try:
            serialized_data = serializers.StreetModelSerializer(models.StreetModel.objects.filter(idCity_id=city_id))
            return Response(serialized_data.data, status=200)
        except Exception:
            return Response(None, status=400)


class HandleShop(APIView):
    @staticmethod
    def get(request):
        street = request.GET.get('street') if request.GET.get('street') != '' else None
        city = request.GET.get('city') if request.GET.get('city') != '' else None
        open = request.GET.get('open') if request.GET.get('open') != '' else None
        try:
            shop_list = models.ShopModel.objects.all()
            shop_list = shop_list.filter(street=street) if street is not None else shop_list
            shop_list = shop_list.filter(city=city) if city is not None else shop_list
            if open != '1' and open != '0' and open is not None:
                raise Exception
            elif open is not None:
                shop_list = shop_list.filter(
                    start__lte=timezone.localtime().time()
                ) & shop_list.filter(
                    end__gte=timezone.localtime().time()
                ) if open == '1' else shop_list
                shop_list = shop_list.filter(
                    start__gte=timezone.localtime().time()
                ) ^ shop_list.filter(
                    end__lte=timezone.localtime().time()
                ) if open == '0' else shop_list

            serialized_data = serializers.ShopModelSerializer(shop_list)
            return Response(serialized_data.data, status=200)
        except Exception:
            return Response(None, status=400)

    @staticmethod
    def post(request):
        request_data = json.loads(request.body)
        try:
            temp = models.ShopModel(
                name=request_data['name'],
                idCity_id=request_data['idCity_id'],
                city=models.CityModel.objects.get(id=request_data['idCity_id']).name,
                idStreet_id=request_data['idStreet_id'],
                street=models.StreetModel.objects.get(id=request_data['idStreet_id']).name,
                building=request_data['building'],
                start=request_data['start'],
                end=request_data['end']
            )
            temp.save()
            return Response(f"id: {temp.id}", status=200)
        except Exception as e:
            print(e)
            return Response(None, status=400)
