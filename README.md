<h1 align="center">Paynet Software Development Kit</h1>

<p align="center">
  <a href="https://t.me/+lO97J78xBj45MzBi">
    <img src="https://img.shields.io/badge/Support%20Group-blue?logo=telegram&logoColor=white" alt="Support Group on Telegram"/>
  </a>
</p>


## Installation

```shell
pip install paynet-pkg
```

## Installation to Django

Add `'paynet'` in to your settings.py

```python
INSTALLED_APPS = [
    ...
    'paynet',
    ...
]
```

Add `'paynet'` credentials inside to settings.py

Paynet configuration settings.py
```python
PAYNET_USERNAME = "your-paynet-username"
PAYNET_PASSWORD = "your-paynet-password"
PAYNET_ACCOUNT_FIELD = "order_id"
PAYNET_ACCOUNT_MODEL = "order.models.Order"
```

Create a new View that about handling call backs
```python
from paynet.views import PaynetWebhook


class PaynetWebhookAPIView(PaynetWebhook):
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
```

Add a `payme` path to core of urlpatterns:

```python
from django.urls import path
from django.urls import include

from your_app.views import PaynetWebhookAPIView

urlpatterns = [
    ...
    path("payment/paynet/update/", PaynetWebhookAPIView.as_view()),
    ...
]
```

Run migrations
```shell
python3 manage.py makemigrations && python manage.py migrate
```

🎉 Congratulations you have been integrated paynet with django, keep reading docs. After successfull migrations check your admin panel and see results what happened.
