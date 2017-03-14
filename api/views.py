from rest_framework import generics
  
from .models import Book
from people.models import Person
from .serializers import BookSerializer
  
class BookList(generics.ListCreateAPIView):
	"""
	API endpoint for listing and creating Book objects
	"""
	queryset = Person.objects.filter(first_name__istartswith='B')
	serializer_class = BookSerializer
    
          
          
          
          
          
