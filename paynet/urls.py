from django.urls import path


from paynet.views import PaynetCallbackAPIView


urlpatterns = [
    path('update', PaynetCallbackAPIView.as_view(), name='paynet-callback'),
]
