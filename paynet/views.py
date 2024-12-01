import base64

from datetime import datetime

from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from paynet import exceptions
from paynet.exceptions import whitelist_errors
from paynet.models import PaynetTransaction as Transaction
from paynet.serializers import GetStatementSerializer
from paynet.serializers import ChangePasswordSerializer
from paynet.serializers import CheckTransactionSerializer
from paynet.serializers import CancelTransactionSerializer
from paynet.serializers import PerformTransactionSerializer


AccountModel = import_string(settings.PAYNET_ACCOUNT_MODEL)


# pylint: disable=E1101,W0718
class PaynetCallbackAPIView(APIView):
    """
    API endpoint for handling incoming paynet webhooks.
    """
    authentication_classes = ()
    allowed_services = [1,]

    def post(self, request):
        """
        Entry point for handling incoming paynet requests.
        """
        data = request.data
        creds = request.headers.get('Authorization')

        rpc_id = data['id']
        method = data['method']
        params = data['params']

        if not self.authenticate_request(creds):
            raise exceptions.InvalidLoginOrPassword(rpc_id=rpc_id)

        if not self.validate_request_format(data):
            raise exceptions.InvalidRPCRequest(rpc_id=rpc_id)

        service_id = params.get('serviceId')
        if not self.is_service_enabled(service_id):
            raise exceptions.ServiceTemporarilyUnavailable(rpc_id=rpc_id)

        try:
            return self.handle_method(method, params, rpc_id)

        except whitelist_errors as exc:
            raise exc

        except ValidationError as exc:
            raise exceptions.MissingRPCParameters(
                rpc_id=rpc_id,
                exc=str(exc)
            ) from exc

        except Exception as exc:
            raise exceptions.InternalSystemError(
                rpc_id=rpc_id,
                exc=str(exc)
            ) from exc

    def authenticate_request(self, creds):
        """
        Validate the Basic Auth credentials.

        Args:
            creds (str): The Authorization header containing Basic Auth credentials.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        if not creds or not creds.startswith('Basic '):
            return False

        try:
            encoded_creds = creds[6:]
            decoded_bytes = base64.b64decode(encoded_creds)
            decoded_string = decoded_bytes.decode('utf-8')
            username, password = decoded_string.split(':', 1)

            return username == settings.PAYNET_USERNAME and password == settings.PAYNET_PASSWORD

        except (ValueError, base64.binascii.Error):
            return False

    def validate_request_format(self, data):
        """
        Validate the request format for JSON-RPC compliance.
        """
        if not isinstance(data, dict):
            return False
        return all(k in data for k in ("jsonrpc", "method", "id", "params"))

    def is_service_enabled(self, service_id) -> bool:
        """
        Check if the service is enabled.
        """
        if service_id not in self.allowed_services:
            return False

        return True

    def handle_method(self, method, params, rpc_id):
        """
        Route the request to the appropriate method handler.
        """
        methods = {
            "PerformTransaction": self.perform_transaction,
            "CheckTransaction": self.check_transaction,
            "CancelTransaction": self.cancel_transaction,
            "GetStatement": self.get_statement,
            "ChangePassword": self.change_password,
            "GetInformation": self.get_information,
        }

        if method not in methods:
            exc = f"method {method} is not supported"
            raise exceptions.MethodNotFound(
                rpc_id=rpc_id,
                exc=exc
            )

        return methods[method](params, rpc_id)

    def perform_transaction(self, params, rpc_id):
        """
        perform a transaction method process
        """
        serializer = PerformTransactionSerializer(data=params)
        serializer.is_valid(raise_exception=True)

        transaction, created = Transaction.objects.get_or_create(
            transaction_id=serializer.validated_data['transactionId'],
            defaults={
                'service_id': serializer.validated_data['serviceId'],
                'account_id': serializer.validated_data['fields'][settings.PAYNET_ACCOUNT_FIELD],
                'amount': serializer.validated_data['amount'],
                'status': Transaction.SUCCESSFUL
            }
        )
        if not created:
            raise exceptions.TransactionAlreadyExists(rpc_id=rpc_id)

        # callback successfully event
        self.successfully_payment(params)

        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "providerTrnId": transaction.id,
                "timestamp": transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "fields": {
                    settings.PAYNET_ACCOUNT_FIELD: transaction.account_id
                }
            }
        })

    def check_transaction(self, params, rpc_id):
        """
        check a transaction method process
        """
        serializer = CheckTransactionSerializer(data=params)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = Transaction.objects.get(
                transaction_id=serializer.validated_data['transactionId'],
                service_id=serializer.validated_data['serviceId']
            )

        except Transaction.DoesNotExist as exc:
            raise exceptions.TransactionNotFound(
                rpc_id=rpc_id, exc=exc
            ) from exc

        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "transactionState": transaction.status,
                "timestamp": transaction.updated_at.strftime('%Y-%m-%d %H:%M:%S'), # noqa
                "providerTrnId": transaction.id
            }
        })

    def cancel_transaction(self, params, rpc_id):
        """
        cancel a transaction method process
        """
        serializer = CancelTransactionSerializer(data=params)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = Transaction.objects.get(
                transaction_id=serializer.validated_data['transactionId'],
                service_id=serializer.validated_data['serviceId']
            )

        except Transaction.DoesNotExist as exc:
            raise exceptions.TransactionNotFound(
                rpc_id=rpc_id, exc=exc
            ) from exc

        if transaction.status == Transaction.CANCELLED:
            raise exceptions.TransactionAlreadyCancelled(
                rpc_id=rpc_id
            )

        if not self.check_balance(transaction.amount):
            raise exceptions.InsufficientFunds()

        transaction.status = Transaction.CANCELLED
        transaction.save()

        # callback cancelled transaction event
        self.cancelled_payment(params)

        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "providerTrnId": transaction.id,
                "timestamp": transaction.updated_at.strftime('%Y-%m-%d %H:%M:%S'), # noqa
                "transactionState": Transaction.CANCELLED
            }
        })

    def check_balance(self, amount) -> bool:
        """
        Check if the amount is within the balance limits.
        you can override this method.
        """
        return amount >= 1

    def get_statement(self, params, rpc_id):
        """
        get a statement method process
        """
        serializer = GetStatementSerializer(data=params)
        serializer.is_valid(raise_exception=True)

        transactions = Transaction.objects.filter(
            service_id=serializer.validated_data['serviceId'],
            created_at__range=[
                serializer.validated_data['dateFrom'],
                serializer.validated_data['dateTo']
            ]
        ).exclude(status=Transaction.CANCELLED)

        statements = [
            {
                "amount": tx.amount,
                "providerTrnId": tx.id,
                "transactionId": tx.transaction_id,
                "timestamp": tx.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for tx in transactions
        ]

        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {"statements": statements}
        })

    def get_information(self, params, rpc_id):
        """
        get information method process
        """
        info_fields = ("id",)
        account_id = params['fields'][settings.PAYNET_ACCOUNT_FIELD]

        if getattr(settings, 'PAYNET_ACCOUNT_INFO_FIELDS', None):
            info_fields = settings.PAYNET_ACCOUNT_INFO_FIELDS

        account = AccountModel.objects\
            .filter(id=account_id).values(*info_fields)

        if not account:
            raise exceptions.ClientNotFound(rpc_id=rpc_id)

        account = account.first()

        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "status": Transaction.CREATED,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "fields": {
                    "id": account
                }
            }
        })

    def change_password(self, params, rpc_id):
        """
        change password method process
        """
        serializer = ChangePasswordSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        return Response({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": "success"
        })

    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        print(f"payment successful params: {params}")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")
