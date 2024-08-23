from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserAddress
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'account_number',
        'balance',
        'account_type',
        'gender',
        'birth_date',
        'initial_deposit_date',
    )
class UserAddressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'division',
        'district',
        'thana',
        'post_code'
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(UserAddress, UserAddressAdmin),