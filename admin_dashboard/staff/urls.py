from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('leadership/edit/', views.edit_my_leadership, name='edit_my_leadership'),
    path('leadership/me/', views.leadership_detail, name='leadership_detail'),
]
