from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_report():
    subject_file = render_to_string('messages/order_report_subject.txt')
    template_file = render_to_string('messages/order_report_html_body.html', )
    # Message should have different txt file,
    # which would carry complete details in text
    send_mail(
        subject=subject_file,
        message=subject_file,
        from_email='sender@partumsolutions.com',
        recipient_list=['receiver@partumsolutions.com'],
        html_message=template_file,
    )
