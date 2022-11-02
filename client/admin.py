from django.contrib import admin
from django.contrib.admin import ModelAdmin

from client.models import ClientAccount, ProductOrder, ProductOrderItem, InstallmentPay, Invoice, InvoiceList


# Register your models here.
class ClientAccountAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'village')


class InstallmentPayAdmin(ModelAdmin):
    list_display = ('client', 'is_pay', 'is_late',)


admin.site.register(ClientAccount, ClientAccountAdmin)
admin.site.register(InstallmentPay, InstallmentPayAdmin)

admin.site.register([ProductOrder, ProductOrderItem, Invoice, InvoiceList])
