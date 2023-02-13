from rest_framework.generics import ListAPIView
from .models import Poin
from .serializers import PoinSerializer
from rest_framework.filters import OrderingFilter, SearchFilter

class ListPoin(ListAPIView):
    serializer_class = PoinSerializer
    queryset = Poin.objects.all()
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("email")