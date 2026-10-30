from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.quote_thanks, name="quote_thanks"),
    path("track/", views.track_event, name="track_event"),
    path("service/<int:pk>/", views.service_detail, name="service_detail"),
    path("branch/<int:pk>/", views.branch_detail, name="branch_detail"),
]
