from django.http import HttpResponse
from django.shortcuts import render

from .models import AModel
from .tasks import send_email_1 as send_email_1_task
from .tasks import send_email_2 as send_email_2_task
from .tasks import send_email_3 as send_email_3_task
from .tasks import send_email_4 as send_email_4_task
from .tasks import send_email_5 as send_email_5_task

# Create your views here.
def send_email(request):
    print("View Sending email...")
    a_model = AModel.objects.first()
    a_model.a_field = "Updated field"
    a_model.save()
    send_email_1_task.send('View Subject 1')
    send_email_2_task.send('View Subject 2')
    send_email_3_task.send('View Subject 3')
    send_email_4_task.send('View Subject 4')
    send_email_5_task.send('View Subject 5')
    print("...email sent (View)")
    return HttpResponse('Success')