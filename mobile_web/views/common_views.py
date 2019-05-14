from django.views.generic import TemplateView
from common.views import RegisterView, LoginView,HomeView, UpdateProfile


class MobileRegisterView(RegisterView):
    template_name = 'mobile_web/register.html'


class MobileLoginView(LoginView):
    template_name = 'mobile_web/login.html'

class MobileLogoutView(TemplateView):
    pass


class MobileHomePageView(HomeView):
    template_name = 'mobile_web/home.html'

class MobileUserInfo(UpdateProfile):
    template_name = 'mobile_web/user.html'
