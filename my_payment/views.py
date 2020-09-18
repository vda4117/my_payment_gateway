from django.shortcuts import render
from rest_framework import viewsets
from django.views import View
from .serializers import *
from .models import *
from .utils import *

import datetime
from uuid import uuid4
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import LoginRequiredMixin, CsrfExemptMixin 

from rest_framework import status
from rest_framework.response import Response

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CyberSourceTransactionViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    queryset = CyberSourceTransaction.objects.all()
    serializer_class = CyberSourceTransactionSerializer

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(course_code=12345)
        # Create a transaction in the database before we pass to CyberSource;
        # we will update this with a timestamp on return from CyberSource
        transaction_uuid = uuid4().hex
        transaction = CyberSourceTransaction()
        transaction.transaction_uuid = transaction_uuid
        transaction.user = self.request.user
        transaction.course = course
        transaction.save()

        # Fields to pass to CyberSource - see manual for a full list
        fields = {}
        fields['profile_id'] = settings.CYBERSOURCE_PROFILE_ID
        fields['access_key'] = settings.CYBERSOURCE_ACCESS_KEY
        fields['amount'] = '10'
        fields['transaction_uuid'] = transaction_uuid
        fields['bill_to_forename'] = "Vishesh"
        fields['bill_to_surname'] = "Agrawal"
        fields['bill_to_email'] = "vishesh.agrawal@ayninfotech.com"
        fields['bill_to_address_city'] = "Amravati"
        fields['bill_to_address_country'] = "AE"
        fields['bill_to_company_name'] = "AYN"
        fields['locale'] = 'en-us'
        fields['currency'] = 'AED'
        fields['transaction_type'] = 'sale'
        fields['reference_number'] = 1000 + transaction.id
        fields['bill_to_address_line1'] = "At Post Amravati, UAE"

        # context = super(CyberSourceTransactionViewSet, self).get_context_data(**kwargs)
        context = {}
        context = sign_fields_to_context(fields, context)

        # Render a page which POSTs to CyberSource via JavaScript.
        return render(
            self.request,
            'my_payment/post_to_cybersource.html',
            context=context,
        )


class CyberSourceResponseViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """
    Recevies a POST from CyberSource and redirects to home.
    """
    queryset = CyberSourceResponse.objects.all()
    serializer_class = CyberSourceResponseSerializer


    def create(self, request, *args, **kwargs):
        # DECISION can be ACCEPT, REVIEW, DECLINE, ERROR, or CANCEL.
        # See page 152: http://apps.cybersource.com/library/documentation/dev_guides/Secure_Acceptance_WM/Secure_Acceptance_WM.pdf
        decision = request.POST.get('decision').upper()
        print(decision)
        print(request.POST.get('req_reference_number'))
        print(request.POST.get('req_transaction_uuid'))

        if decision == 'ACCEPT':
            print(request)
            messages.success(
                request,
                'Your payment was successful and the course has been added.',
            )
            
        else:
            # Uh oh, unsuccessful payment.
            print(request)
            messages.error(
                request,
                'Sorry, your payment was not successful.',
            )

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)