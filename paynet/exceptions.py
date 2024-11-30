"""
the paynet exceptions
"""
import logging

from rest_framework import status
from rest_framework.exceptions import APIException


logger = logging.getLogger(__name__)


# pylint: disable=W1203

class JSONRPCException(APIException):
    """
    Base exception class for JSON-RPC 2.0 formatted errors.
    Ensures that all exceptions return a JSON-RPC compliant structure.
    """
    code = None

    # pylint: disable=super-init-not-called
    def __init__(self, detail=None, code=None, rpc_id=None, exc=None):
        """
        Initialize the exception with custom detail, code, and JSON-RPC ID.
        
        Args:
            detail (str): Custom error message.
            code (int): Error code (overrides default code).
            rpc_id (int): JSON-RPC ID for the request.
        """
        self.status_code = status.HTTP_200_OK
        self.detail = {
            "jsonrpc": "2.0",
            "id": rpc_id or None,
            "error": {
                "code": self.code,
                "message": detail or self.default_detail
            }
        }
        logger.error(f"Paynet RPC error detail: {self.detail} exc: {exc}")


# Error implementations
class MethodNotPOST(JSONRPCException):
    """
    Exception raised when the HTTP method is not POST.
    """
    code = -32300
    default_detail = "Request method must be POST."


class JSONParsingError(JSONRPCException):
    """
    Exception raised when there is an error parsing the JSON request.
    """
    code = -32700
    default_detail = "Error parsing JSON."


class InvalidRPCRequest(JSONRPCException):
    """
    Exception raised when the RPC request is missing required fields 
    or fields have invalid types.
    """
    code = -32600
    default_detail = "Required fields are missing or have invalid types in the RPC request."


class MethodNotFound(JSONRPCException):
    """
    Exception raised when the requested RPC method does not exist.
    """
    code = -32601
    default_detail = "Requested method not found."


class MissingRPCParameters(JSONRPCException):
    """
    Exception raised when required parameters are missing in the request.
    """
    code = -32602
    default_detail = "Missing required fields in parameters."


class InternalSystemError(JSONRPCException):
    """
    Exception raised when an internal system error occurs.
    Typically used for database or file system failures.
    """
    code = -32603
    default_detail = "System error due to internal failure."


class OperationCompletedSuccessfully(JSONRPCException):
    """
    Exception raised to indicate that the operation was completed successfully.
    """
    code = 0
    default_detail = "Operation completed successfully."


class InsufficientFunds(JSONRPCException):
    """
    Exception raised when a client has insufficient funds to cancel a payment.
    """
    code = 77
    default_detail = "Insufficient funds to cancel payment."


class ServiceTemporarilyUnavailable(JSONRPCException):
    """
    Exception raised when the requested service is temporarily unavailable.
    """
    code = 100
    default_detail = "Service temporarily unavailable."


class QuotaExceeded(JSONRPCException):
    """
    Exception raised when the user has exceeded their quota.
    """
    code = 101
    default_detail = "Quota exceeded."


class SystemErrorExc(JSONRPCException):
    """
    Exception raised for a generic system error.
    """
    code = 102
    default_detail = "System error."


class UnknownError(JSONRPCException):
    """
    Exception raised for an unknown error.
    """
    code = 103
    default_detail = "Unknown error."


class WalletNotIdentified(JSONRPCException):
    """
    Exception raised when the wallet cannot be identified.
    """
    code = 113
    default_detail = "Wallet not identified."


class MonthlyLimitExceeded(JSONRPCException):
    """
    Exception raised when the monthly limit for an account is exceeded.
    """

    code = 140
    default_detail = "The monthly limit is exceeded for this account."


class DailyLimitExceeded(JSONRPCException):
    """
    Exception raised when the daily limit for an account is exceeded.
    """
    code = 141
    default_detail = "The daily limit is exceeded for this account."


class TransactionAlreadyExists(JSONRPCException):
    """
    Exception raised when attempting to create a transaction that already exists.
    """
    code = 201
    default_detail = "Transaction already exists."


class TransactionAlreadyCancelled(JSONRPCException):
    """
    Exception raised when a transaction that is already cancelled
    is attempted to be cancelled again.
    """
    code = 202
    default_detail = "Transaction already cancelled."


class TransactionNotFound(JSONRPCException):
    """
    Exception raised when a requested transaction cannot be found.
    """
    code = 203
    default_detail = "Transaction not found."


class NumberDoesNotExist(JSONRPCException):
    """
    Exception raised when a specified number does not exist.
    """
    code = 301
    default_detail = "Number does not exist."


class ClientNotFound(JSONRPCException):
    """
    Exception raised when a specified client cannot be found.
    """
    code = 302
    default_detail = "Client not found."


class ProductNotFound(JSONRPCException):
    """
    Exception raised when a specified product cannot be found.
    """
    code = 304
    default_detail = "Product not found."


class ServiceNotFound(JSONRPCException):
    """
    Exception raised when a specified service cannot be found.
    """
    code = 305
    default_detail = "Service not found."


class RequiredParametersMissing(JSONRPCException):
    """
    Exception raised when one or more required parameters are missing in the request.
    """
    code = 411
    default_detail = "One or more required parameters are missing."


class InvalidLoginOrPassword(JSONRPCException):
    """
    Exception raised for invalid login or password.
    """
    code = 412
    default_detail = "Invalid login or password."


class InvalidAmount(JSONRPCException):
    """
    Exception raised when the provided amount is invalid.
    """
    code = 413
    default_detail = "Invalid amount."


class InvalidDateTimeFormat(JSONRPCException):
    """
    Exception raised when the provided date and time format is invalid.
    """
    code = 414
    default_detail = "Invalid date and time format."


class AmountExceedsLimit(JSONRPCException):
    """
    Exception raised when the provided amount exceeds the allowed limit.
    """
    code = 415
    default_detail = "Amount exceeds the maximum limit."


class TransactionsProhibited(JSONRPCException):
    """
    Exception raised when transactions are prohibited for a specific payer.
    """
    code = 501
    default_detail = "Transactions are prohibited for this payer."


class AccessDenied(JSONRPCException):
    """
    Exception raised when access is denied to a resource or operation.
    """
    code = 601
    default_detail = "Access denied."


class InvalidCommandCode(JSONRPCException):
    """
    Exception raised when an invalid command code is provided.
    """
    code = 603
    default_detail = "Invalid command code."


whitelist_errors = (
    MethodNotPOST,
    JSONParsingError,
    InvalidRPCRequest,
    MethodNotFound,
    MissingRPCParameters,
    InternalSystemError,
    OperationCompletedSuccessfully,
    InsufficientFunds,
    ServiceTemporarilyUnavailable,
    QuotaExceeded,
    SystemErrorExc,
    UnknownError,
    WalletNotIdentified,
    MonthlyLimitExceeded,
    DailyLimitExceeded,
    TransactionAlreadyExists,
    TransactionAlreadyCancelled,
    TransactionNotFound,
    NumberDoesNotExist,
    ClientNotFound,
    ProductNotFound,
    ServiceNotFound,
    RequiredParametersMissing,
    InvalidLoginOrPassword,
    InvalidAmount,
    InvalidDateTimeFormat,
    AmountExceedsLimit,
    TransactionsProhibited,
    AccessDenied,
    InvalidCommandCode,
)
