from rest_framework import serializers


# pylint: disable=abstract-method
class PerformTransactionSerializer(serializers.Serializer):
    """
    Serializer for performing a transaction
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    serviceId = serializers.IntegerField()
    transactionId = serializers.IntegerField()
    fields = serializers.JSONField()


class CheckTransactionSerializer(serializers.Serializer):
    """
    Serializer for check transaction
    """
    serviceId = serializers.IntegerField()
    transactionId = serializers.IntegerField()


class CancelTransactionSerializer(serializers.Serializer):
    """
    Serializer for cancel transaction
    """
    serviceId = serializers.IntegerField()
    transactionId = serializers.IntegerField()


class GetStatementSerializer(serializers.Serializer):
    """
    Serializer for get statement
    """
    serviceId = serializers.IntegerField()
    dateFrom = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    dateTo = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for change password
    """
    newPassword = serializers.CharField(max_length=128)
