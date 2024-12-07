import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Transaction
from .utils import sign_message

import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Transaction
from .utils import sign_message
from django.utils.timezone import now
import time
from django.contrib.auth import get_user_model

def payment_page(request):
    if request.method == 'POST':

        # Simulate an authenticated user (replace with an actual user in a real environment)
        User = get_user_model()
        sample_user = User.objects.first()  # Fetch the first user in the database

        # Check if a sample user exists, or create one for testing
        if not sample_user:
            sample_user = User.objects.create(
                username='sample_user',
                email='sample_user@example.com'
            )

        # Generate a unique order ID and initiate payment
        amount = 10.00  # Set a fixed amount for testing
        order_id = f'ORDER-{int(time.time())}'
        transaction = Transaction.objects.create(
            user=sample_user,
            order_id=order_id,
            amount=amount,
            status='Initiated'
        )

        # Prepare FPX B2C fields
        fpx_fields = {
            'fpx_msgType': 'AR',
            'fpx_msgToken': '01',
            'fpx_sellerExId': settings.PAYNET_SELLER_EXCHANGE_ID,
            'fpx_sellerTxnTime': now().strftime('%Y%m%d%H%M%S'),
            'fpx_sellerOrderNo': order_id,
            'fpx_txnCurrency': 'MYR',
            'fpx_txnAmount': f'{amount:.2f}',
            'fpx_version': '7.0',
            'fpx_checkSum': ''
        }

        # Sign the message
        data_to_sign = '|'.join([fpx_fields[key] for key in sorted(fpx_fields) if key != 'fpx_checkSum'])
        fpx_fields['fpx_checkSum'] = sign_message(data_to_sign, settings.PAYNET_CERTIFICATE_PATH)

        # Send request to PayNet FPX
        response = requests.post(settings.PAYNET_ENDPOINT_URL, data=fpx_fields)
        if response.status_code == 200:
            payment_url = response.json().get('payment_url')
            return redirect(payment_url)  # Redirect user to payment gateway
        else:
            transaction.status = 'Failed'
            transaction.save()
            return render(request, 'payment_error.html', {'error': 'Failed to initiate payment.'})

    return render(request, 'payment_page.html')


def payment_callback(request):
    order_id = request.GET.get('fpx_sellerOrderNo')
    status = request.GET.get('fpx_txnStatus')
    transaction = Transaction.objects.get(order_id=order_id)
    if status == '00':
        transaction.status = 'Success'
    else:
        transaction.status = 'Failed'
    transaction.save()
    return render(request, 'payment_result.html', {'transaction': transaction})

