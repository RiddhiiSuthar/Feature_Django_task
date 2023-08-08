from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import Client, License
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

notifications_summary = []

@csrf_exempt
def trigger_emails(request):
    if request.method == 'POST':
        # Trigger email sending job
        summary = send_emails()
        notifications_summary.append(summary) # append the summary details of each client
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"error": "This endpoint only accepts POST requests."}, status=400)

def send_emails():
    clients = Client.objects.all()
    today = timezone.now().date()
    for client in clients:
        expiring_licenses = License.objects.filter(client=client, expiration_datetime__gte=today)
        
        # Condition 1: licenses expiring in exactly 4 months
        licenses_4_months = expiring_licenses.filter(expiration_datetime__lte=today + timedelta(days=120))
        if licenses_4_months.exists():
            send_email_to_admin(licenses_4_months, client)
            return {"info": "licenses expiring in exactly 4 months","client": client.client_name, "admin": client.admin_poc.username}

        # Condition 2: licenses expiring within a month and today is Monday
        licenses_1_month_monday = expiring_licenses.filter(expiration_datetime__lte=today + timedelta(days=30), expiration_datetime__gt=today, expiration_datetime__week_day=1)
        if licenses_1_month_monday.exists():
            send_email_to_admin(licenses_1_month_monday, client)
            return {"info": "licenses expiring in exactly 4 months","client": client.client_name, "admin": client.admin_poc.username}

        # Condition 3: licenses expiring within a week
        licenses_1_week = expiring_licenses.filter(expiration_datetime__lte=today + timedelta(days=7), expiration_datetime__gt=today)
        if licenses_1_week.exists():
            send_email_to_admin(licenses_1_week, client)
            return {"info": "licenses expiring in exactly 4 months","client": client.client_name, "admin": client.admin_poc.username}


def send_email_to_admin(licenses, client):
    subject = "Client Licenses Expiration Notification :client ID Number : {id}".format(id=client.id)
    client_info_template = """
    Client Name: {name}
    Email: {email}
    Phone Number: {phone}
    """.format(name=client.client_name, email=client.poc_contact_email, phone=client.poc_contact_name)

    licenses_template = ''
    for license in licenses:
        licenses_template += """
        License {id}
        - License package: {package}
        - License Type: {license_type}
        - Issued Date: {issued_date}
        - Expiration Date: {expiration_date}
        """.format(id=license.id, package=license.package, license_type=license.license_type, issued_date=license.created_datetime, expiration_date=license.expiration_datetime)

    message = """
    Following licenses are expiring soon for {client_name}:

    {licenses_details}

    Here are the current details of our client:

    {client_details}

    """.format(client_name=client.client_name, licenses_details=licenses_template, client_details=client_info_template)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [client.admin_poc.email])

def home(request):
    global notifications_summary
    return JsonResponse({'summary': notifications_summary})