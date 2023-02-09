from django.shortcuts import render

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Mesin
from .serializers import MesinSerializers

from django.core.exceptions import ObjectDoesNotExist
from bson.objectid import ObjectId
from bson.errors import InvalidId

import sys

# API UNTUK BANYAK MESIN
@api_view(['GET', 'POST'])
def mesinMany(req):
    try:
        
        # menampilkan semua daftar mesin 
        if req.method == 'GET':
            data = Mesin.objects.all()
            mesin = MesinSerializers(data, many=True)

            return JsonResponse({
                'pesan': f'{len(mesin.data)} mesin ditemukan!',
                'data': mesin.data
            }, status = status.HTTP_200_OK)

        # mendaftarkan mesin baru 
        elif req.method == 'POST':
            data = JSONParser().parse(req)
            mesinBaru = MesinSerializers(data=data)

            # cek validasi lalu simpan 
            if mesinBaru.is_valid():
                mesinBaru.save()

                return JsonResponse({
                    'pesan': 'Mesin baru berhasil ditambahkan',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(mesinBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)

    except:
        print(sys.exc_info())        

        return JsonResponse({
            'pesan': 'Internal server bermasalah'
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK SATU MESIN 
@api_view(['GET', 'PUT', 'DELETE'])
def mesinOne(req, identifier):
    
    try:

        # ambil data satu mesin 
        data = Mesin.objects.get(pk=ObjectId(identifier))

        # tampilkan data satu mesin 
        if req.method == 'GET':
            mesin = MesinSerializers(data)

            return JsonResponse({
                'pesan': f'Mesin ditemukan',
                'data': mesin.data
            }, status = status.HTTP_200_OK)

        # edit data satu mesin 
        elif req.method == 'PUT':
            dataBaru = JSONParser().parse(req)
            mesinBaru = MesinSerializers(data, data=dataBaru, partial=True)

            # cek validasi data 
            if mesinBaru.is_valid():
                mesinBaru.save()

                return JsonResponse({
                    'pesan': 'Mesin berhasil diperbaharui'
                }, status = status.HTTP_200_OK)

            # data tidak valid 
            print(mesinBaru.errors)

            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)
        
        elif req.method == 'DELETE':
            data.delete()

            return JsonResponse({
                'pesan': 'Mesin berhasil dihapus!'
            }, status = status.HTTP_200_OK)
        
    except (InvalidId, ObjectDoesNotExist):
        return JsonResponse({
            'pesan': 'Mesin tidak ditemukan',
            'data': {}
        }, status = status.HTTP_404_NOT_FOUND)
    
    except:
        # jika sistem error 
        print(sys.exc_info())

        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK SCAN QR 
@api_view(['PUT'])
def scanMesin(req):
    try:
        # ambil data satu mesin 
        body = JSONParser().parse(req)

        data = Mesin.objects.get(pk=ObjectId(body['id_mesin']))

        if body['id_pengguna'] != '' :
            tesUserId = ObjectId(body['id_pengguna'])

        mesinBaru = MesinSerializers(data, data={'id_pengguna_aktif': body['id_pengguna']}, partial=True)

        # cek validasi data 
        if mesinBaru.is_valid():
            mesinBaru.save()

            return JsonResponse({
                'pesan': 'Scan mesin berhasil'
            }, status = status.HTTP_200_OK)

        # data tidak valid 
        print(mesinBaru.errors)

        return JsonResponse({
            'pesan': 'Cek kembali data yang anda masukkan!',
        }, status = status.HTTP_400_BAD_REQUEST)

    except (InvalidId, ObjectDoesNotExist):
        return JsonResponse({
            'pesan': 'id mesin atau pengguna tidak valid',
            'data': {}
        }, status = status.HTTP_404_NOT_FOUND)
    
    except:
        # jika sistem error 
        print(sys.exc_info())

        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

