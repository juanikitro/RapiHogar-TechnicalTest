from .models import Company, User, Scheme, Pedido
from django.contrib import admin
from .models import Company

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Scheme)
admin.site.register(Pedido)

