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

class ListPoin(ListAPIView):
    serializer_class = PoinSerializer
    queryset = Poin.objects.all()
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("email")

@api_view(["GET"])
def getPoin(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user_id = User.objects.get(_id=ObjectId(payload['id']))._id
    poin = Poin.objects.filter(id_user = user_id).first()
    serializer = PoinSerializer(poin)
    return Response(serializer.data)