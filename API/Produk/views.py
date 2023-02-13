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

from .models import Produk, Kategori, Penukaran
from Account.models import User
from API.Poin.models import Poin
from API.Poin.serializers import PoinSerializer
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
        
# PENUKARAN 
class ManyPenukaran(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    serializer_class = PenukaranSerializer
    queryset = Penukaran.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['nama', 'kode']
    ordering_fields = ['-created']

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
        try:
            pesanan = JSONParser().parse(request)

            produk = Produk.objects.get(pk = ObjectId(pesanan['id_produk']))
            produkData = ProdukSerializers(produk).data

            user = Poin.objects.get(id_user = pesanan['id_pengguna'])
            userData = PoinSerializer(user).data
            
            biaya = produkData['harga'] * pesanan['jumlah']

            if userData['poin'] < biaya:
                return Response({
                    'message': f'Your points are not enough',
                }, status = status.HTTP_406_NOT_ACCEPTABLE)

            invoice = {
                'id_pengguna': pesanan['id_pengguna'],
                'id_produk': pesanan['id_produk'],
                'nama': userData['nama'],
                'email': userData['email'],
                'kode': str("".join(random.choice(string.ascii_letters + string.digits ) for x in range(12))),
                'produk': produkData['nama'],
                'jumlah': pesanan['jumlah'],
                'biaya': biaya,
                'selesai': False
            }
            
            invoiceData = PenukaranSerializer(data = invoice)
            
            if invoiceData.is_valid():
                invoiceData.save()

                return Response({
                    'message': 'Redeem added to queue',
                }, status = status.HTTP_201_CREATED)                    
            
            print(invoiceData.errors)
            return Response({
                'message': 'Redeem failure',
            }, status = status.HTTP_400_BAD_REQUEST) 

        except (InvalidId, ObjectDoesNotExist):
            return Response({
                'message': 'Not found!',
            }, status = status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'DELETE'])
def OnePenukaran(req, kode):
    try:
        penukaran = Penukaran.objects.get(kode = kode)
        penukaranData = PenukaranSerializer(penukaran).data
        
        if req.method == 'DELETE':
            penukaran.delete()

            return Response({
                'message': f'Content deleted',
            }, status = status.HTTP_204_NO_CONTENT)

        elif req.method == 'GET':

            produk = Produk.objects.get(pk = ObjectId(penukaranData['id_produk']))
            produkData = ProdukSerializers(produk).data

            # user = User.objects.get(_id = penukaranData['id_pengguna'])
            # userData = UserSerializer(user).data
            
            poinUser = Poin.objects.get(id_user = penukaranData['id_pengguna'])
            poinUserData = PoinSerializer(poinUser).data
            
            if poinUserData['poin'] < penukaranData['biaya']:
                return Response({
                    'message': f'Point is not enough',
                }, status = status.HTTP_406_NOT_ACCEPTABLE)

            if penukaranData['jumlah'] > produkData['stok']:
                return Response({
                    'message': f'Product stock is not enough',
                }, status = status.HTTP_406_NOT_ACCEPTABLE)

            penukaranUpdate = PenukaranSerializer(penukaran, data={'selesai': True}, partial=True)
            produkUpdate = ProdukSerializers(produk, data={
                'stok': produkData['stok'] - penukaranData['jumlah'],
                'penukar': produkData['penukar'] + 1
                }, partial=True)
            userUpdate = PoinSerializer(poinUser, data={'poin': poinUserData['poin'] - penukaranData['biaya']}, partial=True)

            if penukaranUpdate.is_valid() and produkUpdate.is_valid() and userUpdate.is_valid():
                penukaranUpdate.save()
                produkUpdate.save()
                userUpdate.save()
                
                return Response({
                    'message': f'Redeem verified',
                }, status = status.HTTP_200_OK)

            return Response({
                'message': f'Verification failure',
            }, status = status.HTTP_200_OK)
            
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
