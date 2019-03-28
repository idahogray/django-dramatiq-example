from django.http import HttpResponse
from django.shortcuts import render

from .tasks import send_email as send_email_task

# Create your views here.
def send_email(request):
    print("View Sending email...")
    send_email_task.send('View Subject')
    print("...email sent (View)")
    return HttpResponse('Success')