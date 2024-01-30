from django.contrib import admin
from .models import Pharmacy
from.models import user,product,booking,cart,Login
from django.contrib.auth.models import Group, User
# Register your models here.













admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Pharmacy)
admin.site.register(user)
admin.site.register(product)
admin.site.register(booking)
admin.site.register(cart)
admin.site.register(Login)

admin.site.site_header = 'E Pharma'

