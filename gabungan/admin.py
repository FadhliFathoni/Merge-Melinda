from django.contrib import admin
from Account.models import Account
from API.Mesin.models import Mesin
from API.Minyak.models import Minyak
from API.Minyak.models import Poin
from API.Produk.models import Kategori,Penukaran,Produk
from API.Transaction.models import Transaksi

admin.site.register(Account)
admin.site.register(Mesin)
admin.site.register(Minyak)
admin.site.register(Poin)
admin.site.register(Kategori)
admin.site.register(Penukaran)
admin.site.register(Produk)
admin.site.register(Transaksi)