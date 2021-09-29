from django.urls import path

from accounts.api.v1.views import DeviceApiView, LoginAPIView, UserRecordRetrieveAPIView

app_name = 'accounts-api-v1'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user-record/', UserRecordRetrieveAPIView.as_view(), name='user-record-item'),
    path('device-id/', DeviceApiView.as_view(), name='check-device'),
]
