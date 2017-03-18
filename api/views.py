from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions
  
from .models import Book
from .serializers import BookSerializer
from trees.views import Planting

from django.http import JsonResponse
  
class BookList(generics.ListCreateAPIView):
	"""
	API endpoint for listing and creating Book objects
	"""
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(BookList, self).dispatch(request, *args, **kwargs)
	
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
		  
		  
def planting_data(request):
	planting = Planting()
	visits = planting.get_visits(purpose=1)
	formset_html = planting.get_form_html(purpose=1)
	return JsonResponse({'formset_html': formset_html})
	
		  
def book_list(request):
	print 'Meth', request.method
		
	queryset = Book.objects.all()
	
	serializer = BookSerializer(data=queryset)
	if serializer.is_valid():
		# serializer.save()
		return JsonResponse(serializer.data)
	return JsonResponse(serializer.errors, status=400)
