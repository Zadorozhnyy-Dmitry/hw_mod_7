from django.contrib import admin

from users.models import Payment, User, Subs


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "paid_date",
        "course",
        "lesson",
        "amount",
        "method",
    )


@admin.register(Subs)
class SubsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course',)
