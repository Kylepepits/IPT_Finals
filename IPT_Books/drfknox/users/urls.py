from django.urls import path
from knox import views as knox_views
from . import views
from .views import BookCreateView, BookListView, RentBookView, ReturnBookView,UserListView

urlpatterns = [
    path('user/', views.get_user),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('rentals/create/', RentBookView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('rentals/<int:rental_id>/return/', ReturnBookView.as_view(), name='return_book'),
    path('my-rentals/', views.MyRentalListView.as_view(), name='my-rentals'),
]
