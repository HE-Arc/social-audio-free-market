from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def send_password_reset_link(
        sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': '{0}/reset_password/{1}'.format(
            settings.CLIENT_APP_URL,
            reset_password_token.key),
        'token_expiration': settings.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME,
    }

    email_html_message = render_to_string(
        'email/user_reset_password.html', context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # Title
        'SAFMarket - Password Reset',
        # Message
        email_plaintext_message,
        # From
        'use-a-password-manager@safmarket.com',
        # To
        [reset_password_token.user.email]
    )

    msg.attach_alternative(email_html_message, 'text/html')
    msg.send()
