from rest_framework.generics import ListAPIView
from .models import Poin
from .serializers import PoinSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view
import jwt
from bson.objectid import ObjectId
from Account.serializers import UserSerializer
from Account.models import User
from rest_framework.exceptions import AuthenticationFailed

from helpers.permissions import has_access

class ListPoin(ListAPIView):
    serializer_class = PoinSerializer
    queryset = Poin.objects.all()
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("email")

@api_view(["GET"])
def getPoin(request):
    if not has_access(request, '*'): raise AuthenticationFailed('Unauthenticated: you are not allowed')

    # user_id = User.objects.get(_id=ObjectId(request.account['id']))._id
    
    poin = Poin.objects.filter(id_user = str(request.account['id'])).first()
    serializer = PoinSerializer(poin)
    return Response(serializer.data)