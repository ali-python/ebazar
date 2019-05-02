from django.views.generic import TemplateView


class MobileRegisterView(TemplateView):
    pass


class MobileLoginView(TemplateView):
    pass


class MobileLogoutView(TemplateView):
    pass


class MobileHomePageView(TemplateView):
    template_name = 'mobile_web/home.html'
