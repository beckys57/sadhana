from django.shortcuts import render
from django.template.loader import render_to_string

from .models import Person

# Create your views here.
def master_list(request):
    people = Person.objects.all().prefetch_related('trees')
    s
    table_context = {
        'people': people,
    return render(request, 'people/master_list.html', contet)
    people_table = render_to_string('people/people_table.html', table_context)
    
    context = {
        'people_table': people_table,
    }
    return render(request, 'people/master_list.html', context)