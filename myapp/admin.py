from django.contrib import admin
from .models import Pharmacy
from.models import user,product,booking,Login, Prescription
from django.contrib.auth.models import Group, User
# Register your models here.
admin.site.register(Prescription)

class LoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'type')
    list_filter = ('status', 'type')
    search_fields = ('username', 'type')

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'loginid', 'email', 'address', 'phone_no')
    search_fields = ('name', 'email')
    list_filter = ('loginid__status',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'loginid', 'address', 'email', 'phone_no')
    search_fields = ('name', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('medicinename','pharmacyid', 'price', 'company', 'type', 'quantity')
    search_fields = ('medicinename', 'company')
    list_filter = ('pharmacyid', 'type')
    readonly_fields = ('pharmacyid', 'medicinename', 'price', 'company', 'type', 'quantity')



class BookingAdmin(admin.ModelAdmin):

    list_display = ('get_pharmacy_name', 'name', 'medicinename', 'date', 'quantity', 'total_amount')
    search_fields = ('name__name', 'medicinename__medicinename')
    list_filter = ('name__loginid__status',)
    readonly_fields = ('get_pharmacy_name', 'name', 'medicinename', 'date', 'quantity', 'total_amount')  
    def get_pharmacy_name(self, obj):
        return obj.medicinename.pharmacyid.name if obj.medicinename and obj.medicinename.pharmacyid else ''

    get_pharmacy_name.short_description = 'Pharmacy'

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'cart_id' in fields:
            fields.remove('cart_id')
        return fields


admin.site.register(Login, LoginAdmin)
admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(user, UserAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(booking, BookingAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = 'E Pharma'

