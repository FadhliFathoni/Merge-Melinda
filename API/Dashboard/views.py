from API.Minyak.models import Minyak
from Account.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from dateutil.relativedelta import relativedelta

from helpers.permissions import has_access

@api_view(["GET"])
def dashboard(request):
    if not has_access(request, ["is_superAdmin", 'is_adminDesa']): raise AuthenticationFailed('Unauthenticated: you are not allowed')

    now = datetime.now().date()
    minyak = Minyak.objects.filter(status = "Terverifikasi",updated__icontains = now)
    user = User.objects.filter(createdAt__icontains = now)
    setor = Minyak.objects.filter(status = "Terverifikasi", updated__icontains = now)
    totalMinyak = 0
    if "date" in request.GET:
        if request.GET["date"] == "week":
            minyak = Minyak.objects.filter(status="Terverifikasi",updated__range = [now-relativedelta(weeks=1),now])
            setor = Minyak.objects.filter(status = "Terverifikasi", updated__range = [now-relativedelta(weeks=1),now])
            user = User.objects.filter(createdAt__range = [now-relativedelta(weeks=1),now])
        elif request.GET["date"] == "month":
            minyak = Minyak.objects.filter(status="Terverifikasi",updated__range = [now-relativedelta(months=1),now])
            setor = Minyak.objects.filter(status = "Terverifikasi", updated__range = [now-relativedelta(months=1),now])
            user = User.objects.filter(createdAt__range = [now-relativedelta(months=1),now])
        elif request.GET["date"] == "year":
            minyak = Minyak.objects.filter(status="Terverifikasi",updated__range = [now-relativedelta(years=1),now])
            setor = Minyak.objects.filter(status = "Terverifikasi", updated__range = [now-relativedelta(years=1),now])
            user = User.objects.filter(createdAt__range = [now-relativedelta(years=1),now])
    for x in minyak:
        totalMinyak = totalMinyak + x.volume
    totalSetor = len(setor)
    totalUser = len(user)
    context = {
        "minyak":totalMinyak,
        "user":totalUser,
        "verifikasi":totalSetor,
    }
    return Response(context)