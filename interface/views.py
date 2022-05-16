from django.views.generic import TemplateView


# Login Page View
class LoginView(TemplateView):
    template_name = 'interface/login.html'


# Logout Page View
class LogoutView(TemplateView):
    template_name = 'interface/logout.html'
