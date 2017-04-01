from rest_framework import serializers

from .models import Book
from trees.models import Visit

class BookSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Book
		fields = ('title', 'author')

class VisitSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Visit
		fields = ('title', 'author')
