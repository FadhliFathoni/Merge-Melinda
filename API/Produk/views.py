from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from djongo.database import connect

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination, InvalidPage
from rest_framework.filters import OrderingFilter, SearchFilter

from bson.objectid import ObjectId 
from bson.errors import InvalidId

from .models import Produk, Kategori
from .serializers import ProdukSerializers, KategoriSerializers, PenukaranSerializer

import sys
import json
import datetime
from operator import itemgetter
import string
import random

# PRODUK  
class ManyProduk(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    serializer_class = ProdukSerializers
    queryset = Produk.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['nama', 'keterangan', 'kategori']

    def get(self, request):
        queryset = self.get_queryset()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer_class = self.serializer_class(result_page, many=True)

        for item in serializer_class.data:
            item['penukaran'] = json.loads(item['penukaran'].replace('\'','\"'))

        return paginator.get_paginated_response(serializer_class.data)
        
class OneProduk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = ProdukSerializers
    queryset = Produk.objects.all()

    def get(self, request, pk, *args, **kwargs):
        try: 
            queryset = Produk.objects.get(pk=ObjectId(pk))
            serializer = self.serializer_class(queryset)

            produkData = serializer.data
            produkData['penukaran'] = json.loads(serializer.data['penukaran'].replace('\'','\"'))
        
            return Response({'result': produkData})

        except (InvalidId, ObjectDoesNotExist) :
            return Response({
                'message': 'Not found!',
                'result': False
            }, status = status.HTTP_404_NOT_FOUND)     

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# KATEGORI
class ManyKategori(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    serializer_class = KategoriSerializers
    queryset = Kategori.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['nama']

    def get(self, request):
        queryset = self.get_queryset()
        
        paginator = PageNumberPagination()
        paginator.page_size = 1

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer_class = self.serializer_class(result_page, many=True)

        return paginator.get_paginated_response(serializer_class.data)

    def post(self, request):
        self.create(request)
        
        return Response({
            'message': 'Added successfully',
        }, status = status.HTTP_201_CREATED) 
        
class OneKategori(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = KategoriSerializers
    queryset = Kategori.objects.all()

    def get(self, request, pk, *args, **kwargs):
        try: 
            self.kwargs['pk'] = ObjectId(self.kwargs['pk'])
            return self.retrieve(request, *args, **kwargs)

        except (InvalidId, ObjectDoesNotExist) :
            return Response({'message': 'Not found!','result': False}, status = status.HTTP_404_NOT_FOUND)     

    def put(self, request, *args, **kwargs):
        try: 
            self.kwargs['pk'] = ObjectId(self.kwargs['pk'])
            return self.partial_update(request, *args, **kwargs)

        except (InvalidId, ObjectDoesNotExist) :
            return Response({'message': 'Not found!','result': False}, status = status.HTTP_404_NOT_FOUND)     

    def delete(self, request, *args, **kwargs):
        try: 
            self.kwargs['pk'] = ObjectId(self.kwargs['pk'])
            self.destroy(request, *args, **kwargs)

            return Response({
                'message': 'Deleted successfully',
            }, status = status.HTTP_204_NO_CONTENT) 

        except (InvalidId, ObjectDoesNotExist) :
            return Response({'message': 'Not found!','result': False}, status = status.HTTP_404_NOT_FOUND)     

# API UNTUK BANYAK PRODUK 
@api_view(['POST'])
def createProduk(req):
    try: 
        data = JSONParser().parse(req)
        
        data["kategori"] = ','.join(data["kategori"])

        produkBaru = ProdukSerializers(data=data)

        # cek validasi lalu simpan 
        if produkBaru.is_valid():
            produkBaru.save()

            return JsonResponse({
                'pesan': 'Produk baru berhasil ditambahkan',
            }, status = status.HTTP_200_OK)
        
        # data yg dikirimkan invalid 
        print(produkBaru.errors)
            
        return JsonResponse({
            'pesan': 'Cek kembali data yang anda masukkan!',
        }, status = status.HTTP_400_BAD_REQUEST)
            
    except:
        print(sys.exc_info())
        
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK SATU KATEGORI 
@api_view(['GET', 'PUT', 'DELETE'])    
def produkOne(req, identifier):
    
    try:
        # ambil dulu satu produk
        data = Produk.objects.get(pk=ObjectId(identifier))

        # dapatkan produk
        if req.method == 'GET':
            produk = ProdukSerializers(data)

            produkData = produk.data
            produkData['penukaran'] = json.loads(produk.data['penukaran'].replace('\'','\"'))

            return JsonResponse({
                'pesan': f'Produk ditemukan',
                'data': produkData,
            }, status = status.HTTP_200_OK)
        
        # edit produk 
        elif req.method == 'PUT':
            dataBaru = JSONParser().parse(req)
            
            if 'kategori' in dataBaru:
                dataBaru["kategori"] = ','.join(dataBaru["kategori"])
            
            produkBaru = ProdukSerializers(data, data=dataBaru, partial=True)

            # cek validasi data 
            if produkBaru.is_valid():
                produkBaru.save()

                return JsonResponse({
                    'pesan': 'Produk berhasil diperbaharui',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(produkBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)
                
        # hapus produk
        elif req.method == 'DELETE':
            data.delete()

            return JsonResponse({
                'pesan': 'Produk berhasil di hapus!'
            })
          
    except (InvalidId, ObjectDoesNotExist) :
        return JsonResponse({
            'pesan': 'Produk tidak ditemukan!',
            'data': []
        }, status = status.HTTP_404_NOT_FOUND)     

    except:
        # jika sistem error 
        print(sys.exc_info())
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK REDEEM 
@api_view(['POST', 'PUT'])
def tukarPoin(req):
    try:
        pesanan = JSONParser().parse(req)
        produk = Produk.objects.get(pk=ObjectId(pesanan['id_produk']))
        produkData = ProdukSerializers(produk).data
        
        if req.method == 'POST':
            userDB = connect('default').get_database('melinda').get_collection('pengguna') 

            biaya = produkData['harga'] * pesanan['jumlah']
            
            produkBaru = produkData
            
            penukaranBaru = json.loads(produkBaru['penukaran'].replace('\'','\"'))
            kodeBaru = str("".join(random.choice(string.ascii_letters + string.digits ) for x in range(7)))

            penukaranBaru[0]['_id'] = ObjectId()
            
            penukaranBaru.append({
                '_id': ObjectId(),
                'id_pengguna': ObjectId(pesanan['id_pengguna']),
                'kode': kodeBaru,
                'jumlah': pesanan['jumlah'],
                'tanggal': datetime.datetime.now(),
                'selesai':  False
            })
            
            # perbaharui stok dan daftar penukaran 
            produkBaru['penukaran'] = penukaranBaru
            produkBaru['stok'] = produkBaru['stok'] - pesanan['jumlah']

            updateProduk = ProdukSerializers(produk, data=produkBaru)

            # cek validasi data 
            if updateProduk.is_valid():
                updateProduk.save()

                print("stok dan penukaran berhasil diperbaharui")
            
            else:
                # data yg dikirimkan invalid 
                print(updateProduk.errors)
                return JsonResponse({
                    'pesan': 'Penukaran gagal!'
                }, status = status.HTTP_503_SERVICE_UNAVAILABLE)

            user = userDB.find_one_and_update({'_id': ObjectId(pesanan['id_pengguna'])}, { '$inc': {'poin': -biaya}})        

            return JsonResponse({
                'pesan': 'Penukaran berhasil!'
            }, status = status.HTTP_200_OK)

        elif req.method == 'PUT':
            produknya = produkData
            
            penukarannya = json.loads(produknya['penukaran'].replace('\'','\"'))
            findPenukaran = list(filter(lambda item: item['kode'] == pesanan['kode'], penukarannya))

            if len(findPenukaran) == 0:
                return JsonResponse({
                    'pesan': 'Kode penukaran tidak ditemukan!'  
                }, status = status.HTTP_404_NOT_FOUND)

            indexPenukaran = penukarannya.index(findPenukaran[0])

            penukarannya[indexPenukaran]['selesai'] = pesanan['selesai']
            produknya['penukaran'] = penukarannya

            updateProduk = ProdukSerializers(produk, data=produknya, partial=True)

            if updateProduk.is_valid():
                
                updateProduk.save()
                
                return JsonResponse({
                    'pesan': 'Status penukaran berhasil diperbaharui'
                }, status = status.HTTP_200_OK)  
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)  
            
    except InvalidId:
        return JsonResponse({
            'pesan': 'Produk atau pengguna tidak ditemukan!',
            'data': []
        }, status = status.HTTP_404_NOT_FOUND)     

    except:
        print(sys.exc_info())
        
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
      