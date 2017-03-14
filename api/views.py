from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
  
from .models import Book
from .serializers import BookSerializer


from django.http import JsonResponse
  
class BookList(generics.ListCreateAPIView):
	"""
	API endpoint for listing and creating Book objects
	"""
	@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ChromeLoginView, self).dispatch(request, *args, **kwargs)
	
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	#	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
		  
		  
		  
		  
@csrf_exempt
def book_list(request):
	print 'Meth', request.method
		
	queryset = Book.objects.all()
	
	serializer = BookSerializer(data=queryset.first().__dict__)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data)
	return JsonResponse(serializer.errors, status=400)
