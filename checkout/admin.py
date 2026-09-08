from django.contrib import admin
from .models import DeliveryCost, Order, OrderLineItem


# resources for TabularInline:
# https://medium.com/django-unleashed/mastering-django-inline-admin-tabularinline-and-stackedinline-examples-c9f17accde84
class OrderLineItemAdminInline(admin.TabularInline):
    """
    Displays each Order's line items inline within the Order's own
    admin page, rather than as a separate section, so the business
    owner sees the full order (buyer, address, items) in one place.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order, including its line items inline,
    read-only system generated fields, and a list view showing the
    columns the business owner needs to see new orders at a glance.
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'stripe_pid')
    list_display = (
        'order_number', 'date', 'full_name', 'shipping_method', 'shipped_at',
    )
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryCost)
