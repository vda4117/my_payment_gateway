from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='CourseModel')
router.register(r'cybersourcetransaction', CyberSourceTransactionViewSet, basename='CyberSourceTransactionModel')
router.register(r'orders/payment-response', CyberSourceResponseViewSet, basename='add-course-cybersource-response')


urlpatterns = [
    path('', include(router.urls)),
    # path('orders/payment-response/', CyberSourceResponseViewSet.as_view(), name='add-course-cybersource-response'),
]