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

from .models import Mesin 
from .serializers import MesinSerializers

import sys
import json
import datetime
from operator import itemgetter
import string
import random

# MESIN
class ManyMesin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    serializer_class = MesinSerializers
    queryset = Mesin.objects.all()
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

class OneMesin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = MesinSerializers
    queryset = Mesin.objects.all()
    
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
   
# API UNTUK SCAN QR 
@api_view(['PUT'])
def scanMesin(req):
    try:
        # ambil data satu mesin 
        body = JSONParser().parse(req)

        data = Mesin.objects.get(pk=ObjectId(body['id_mesin']))

        mesinBaru = MesinSerializers(data, data={'id_pengguna_aktif': body['id_pengguna']}, partial=True)
        msg = 'failure'
        statuss = status.HTTP_404_NOT_FOUND
        
        # cek validasi data 
        if mesinBaru.is_valid():
            mesinBaru.save()
            msg = 'successfully'
            statuss = status.HTTP_200_OK 

        return Response({
            'message': f'Scan {msg}',
        }, status = statuss) 

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

