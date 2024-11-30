from django.contrib import admin


from paynet.utils import get_admin_model
from paynet.models import PaynetTransaction


ModelAdmin = get_admin_model(name="unfold")


class PaynetTransactionUI(ModelAdmin):
    """
    Admin Model for Transaction
    """
    list_display = (
        'id',
        'amount',
        'account_id',
        'transaction_id',
        'service_id',
        'status',
        'created_at',
        'updated_at'
    )


admin.site.register(PaynetTransaction, PaynetTransactionUI)
