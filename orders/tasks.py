# from celery import task
from django.core.mail import send_mail, EmailMessage
from .models import Order

from io import BytesIO
import os
from xhtml2pdf import pisa
from django.template.loader import get_template

from credentials import readcredentials
my_credentials = readcredentials.readcredentials()


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

# @task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created. The e-mail notification will include a .pdf
    confirming the order
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name,
                order.id)

    template_path = 'orders/order/orderconfirmation.html'
    context = {'order': order}
    attachment = render_to_pdf(template_path, context)

    email = EmailMessage(subject,
                         message,
                         my_credentials[1],
                         [order.email])

    email.attach('order_{}.pdf'.format(order.id),
                 attachment,
                 'application/pdf')
    email.send()

    return None
