from django.db import models


class PaynetTransaction(models.Model):
    """
    Represents a transaction made by a user on a specific service.
    
    """
    CREATED = 0
    SUCCESSFUL = 1
    CANCELLED = 2
    NOT_FOUND = 3

    STATUS_CHOICES = [
        (SUCCESSFUL, 'Successfully completed'),
        (CANCELLED, 'Cancelled transaction'),
        (NOT_FOUND, 'Transaction not found'),
    ]
    amount = models.IntegerField()
    account_id = models.BigIntegerField()
    transaction_id = models.BigIntegerField(unique=True)
    service_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_FOUND)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
