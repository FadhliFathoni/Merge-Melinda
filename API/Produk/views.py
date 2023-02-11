from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from djongo.database import connect

from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination, InvalidPage
from rest_framework.filters import OrderingFilter, SearchFilter

from bson.objectid import ObjectId 
from bson.errors import InvalidId

from .models import Produk, Kategori
from Account.models import Account
from API.ManagementUser.serializers import UserSerializer
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
    parser_classes = [MultiPartParser]

    def get(self, request):
        queryset = self.get_queryset()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer_class = self.serializer_class(result_page, many=True)

        # for item in serializer_class.data:
        #     item['penukaran'] = json.loads(item['penukaran'].replace('\'','\"'))

        return paginator.get_paginated_response(serializer_class.data)

    def post(self, request):
        self.create(request)
        
        return Response({
            'message': 'Added successfully',
        }, status = status.HTTP_201_CREATED) 
    
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

# KATEGORI
class ManyKategori(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    serializer_class = KategoriSerializers
    queryset = Kategori.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['nama']
    ordering_fields = ['created']

    def get(self, request):
        queryset = self.get_queryset()
        
        paginator = PageNumberPagination()
        paginator.page_size = 20

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

# API UNTUK REDEEM 
@api_view(['POST', 'PUT'])
def tukarPoin(req):
    try:
        pesanan = JSONParser().parse(req)
        produk = Produk.objects.get(pk=ObjectId(pesanan['id_produk']))
        produkData = ProdukSerializers(produk).data
        
        if req.method == 'POST':
            # userDB = connect('default').get_database('melinda').get_collection('Account_account') 
            user = Account.objects.get(id=pesanan['id_pengguna'])
            userData = UserSerializer(user).data

            biaya = produkData['harga'] * pesanan['jumlah']

            if userData['poin'] < biaya:
                return Response({
                    'message': f'Your points are not enough',
                }, status = status.HTTP_406_NOT_ACCEPTABLE)

            penukaranBaru = produkData['penukaran']
            kodeBaru = str("".join(random.choice(string.ascii_letters + string.digits ) for x in range(7)))
            
            penukaranBaru.append({
                # '_id': ObjectId(),
                'id_pengguna': pesanan['id_pengguna'],
                'kode': kodeBaru,
                'jumlah': pesanan['jumlah'],
                'tanggal': datetime.datetime.now(),
                'selesai':  False
            })
                      
            updateProduk = ProdukSerializers(produk, data={
                    'penukaran': penukaranBaru,
                    'stok': produkData['stok'] - pesanan['jumlah']
                }, partial=True)
            updateUser = UserSerializer(user, data={'poin': userData['poin'] - biaya}, partial=True)
            msg = 'failure'
            statuss = status.HTTP_404_NOT_FOUND
            
            
            # cek validasi data 
            if updateProduk.is_valid() and updateUser.is_valid():
                updateProduk.save()
                updateUser.save()
                
                msg = 'successfully'
                statuss = status.HTTP_200_OK 

            return Response({
                'message': f'Redeem product {msg}',
            }, status = statuss) 
            
        elif req.method == 'PUT':
            # produknya = produkData
            
            # penukarannya = json.loads(produknya['penukaran'].replace('\'','\"'))
            penukarannya = produkData['penukaran']
            findPenukaran = list(filter(lambda item: item['kode'] == pesanan['kode'], penukarannya))

            if len(findPenukaran) == 0:
                raise ObjectDoesNotExist()
                
            indexPenukaran = penukarannya.index(findPenukaran[0])

            # penukarannya[indexPenukaran]['_id'] = ObjectId()
            penukarannya[indexPenukaran]['selesai'] = pesanan['selesai']
            
            # produknya['penukaran'] = penukarannya

            print(penukarannya)
            updateProduk = ProdukSerializers(produk, data={
                'penukaran': penukarannya
                }, partial=True)
            msg = 'failure'
            statuss = status.HTTP_404_NOT_FOUND

            
            if updateProduk.is_valid():
                
                updateProduk.save()

                msg = 'successfully'
                statuss = status.HTTP_200_OK 

            return Response({
                'message': f'Redeem verification {msg}',
            }, status = statuss)  

            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)  
            
    except (InvalidId, ObjectDoesNotExist):
        return Response({
            'message': 'Not found!',
        }, status = status.HTTP_404_NOT_FOUND)
    
    except:
        # jika sistem error 
        print(sys.exc_info())

        return Response({
            'message': 'Internal server ERROR',
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
