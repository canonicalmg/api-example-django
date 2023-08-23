from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorWelcome(TemplateView):
    template_name = 'doctor_welcome.html'

    def __init__(self):
        self.access_token_cache = None
        self.doctor_details_cache = None

    def get_token(self):
        if not self.access_token_cache:
            oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
            self.access_token_cache = oauth_provider.extra_data['access_token']
        return self.access_token_cache

    def make_api_request(self):
        if not self.doctor_details_cache:
            access_token = self.get_token()
            api = DoctorEndpoint(access_token)
            self.doctor_details_cache = next(api.list())
        return self.doctor_details_cache

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs