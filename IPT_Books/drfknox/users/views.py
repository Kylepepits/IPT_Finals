from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import RegisterSerializer, UserSerializer, BookSerializer, RentalSerializer
from rest_framework import generics, permissions, status
from .models import Book, Rental
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from knox.models import AuthToken




def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the user's token
    AuthToken.objects.filter(user=request.user).delete()
    
    return Response({'detail': 'You have been logged out.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def knox_logout(request):
    if request.user.auth_token is not None:
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'})
    else:
        return Response({'message': 'No authentication token found'})


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })


@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_data': serialize_user(user)
        })
    return Response({})
@receiver(post_save, sender=Rental)
def update_book_availability(sender, instance, created, **kwargs):
    if not created:
        # if the rental instance was not just created, it means that it was updated.
        # we only want to update the book availability if the rental was just created.
        return

    # Get the book that was rented
    book = instance.book

    # Set the availability of the book to False
    book.available = False
    book.save()

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RentalCreateView(generics.CreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = []

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Rental

class RentBookView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        user_id = request.user.id
        book = Book.objects.filter(id=book_id, available=True).first()

        if not book:
            return Response({'message': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)

        rental_date = date.today()
        return_due_date = rental_date + timedelta(days=7)

        rental = Rental.objects.create(user_id=user_id, book=book, rental_date=rental_date, return_due_date=return_due_date)

        book.available = False
        book.save()

        return Response({'message': f'Book {book.title} rented successfully', 'rental_id': rental.id})
    
class ReturnBookView(APIView):
    def post(self, request, rental_id):
        rental = get_object_or_404(Rental, id=rental_id)

        # Ensure that the user making the request is the same user who rented the book
        if request.user != rental.user:
            return Response({'error': 'You are not authorized to return this book.'}, status=403)

        # Ensure that the rental hasn't already been returned
        if rental.returned:
            return Response({'error': 'This book has already been returned.'}, status=400)

        # Update the rental object to mark it as returned and set the return date
        rental.returned = True
        rental.return_date = datetime.now()
        rental.save()

        # Set the book availability to True
        book = rental.book
        book.available = True
        book.save()

        return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)
    
class MyRentalListView(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the rentals for the current user
        user = self.request.user
        rentals = Rental.objects.filter(user=user)
        return rentals