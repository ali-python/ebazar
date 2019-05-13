from django.views.generic import TemplateView
from common.views import RegisterView, LoginView,HomeView

class MobileRegisterView(RegisterView):
    template_name = 'mopbile_web/register.html'


class MobileLoginView(LoginView):
    template_name = 'mobile_web/login.html'


class MobileLogoutView(TemplateView):
    pass


class MobileHomePageView(HomeView):
    template_name = 'mobile_web/home.html'
