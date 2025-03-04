from django.urls import path
from . import views
from .views import cancel_ticket

urlpatterns=[
    path('',views.movie_list,name='movie_list'),
    path('<int:movie_id>/theaters',views.theater_list,name='theater_list'),
    path('theater/<int:theater_id>/seats/book/',views.book_seats,name='book_seats'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cancel-ticket/<int:booking_id>/', cancel_ticket, name='cancel_ticket'),
]

 
