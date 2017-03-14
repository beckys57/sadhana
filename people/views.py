from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

from .models import Person, Relationship
from trees.models import Tree, Visit
from trees.views import TreeReport

# Create your views here.
def master_list(request):
    sorting = request.GET.get('sort', 'last_name')
    people = Person.objects.all().order_by(sorting)#.prefetch_related('trees')
    
    planting_list = ''
    pending_plantings = Person.objects.filter(trees__visit__purpose=1)
    if pending_plantings:
        
        planting_list = ''.join([render_to_string('people/person_list_item.html', {'person':person}) for person in pending_plantings])
        print planting_list
        print '**'
        
    table_context = {
        'people': people,
        'sorting': sorting,
    }
    people_table = render_to_string('people/people_table.html', table_context)
    
    context = {
        'people_table': people_table,
        'planting_list': planting_list,
    }
    return render(request, 'people/master_list.html', context)
    
    
def filtered_list_ajax(request):
    if request.is_ajax():
        
        search_term = request.GET.get('query', '')
        filter_code = request.GET.get('filter', '')
        
        print 'Request', search_term
        if search_term:
            split_name = search_term.split(' ')
            if len(split_name) == 1:
                people = Person.objects.filter(Q(last_name__icontains=search_term)|Q(first_name__icontains=search_term))
            else:
                people = Person.objects.filter(Q(last_name__icontains=split_name[1])&Q(first_name__icontains=split_name[0]))
        elif filter_code:
            if filter_code == '1':
                people = Person.objects.prefetch_related('trees').filter(training_date__isnull=False, trees__isnull=False)
        else:
            people = Person.objects.all()
            
        
        context = {
            'people': people,
        }
        
        if request.GET.get('mini', False):
            people_html = render_to_string('people/autocomplete.html', context)
        else:
            people_html = render_to_string('people/people_table.html', context)
        
        return JsonResponse({'success': 'Got list of people', 'html': people_html})
        
        
def make_list_item_ajax(request):
    if request.is_ajax():
        person_id = search_term = request.GET.get('person_id')
        person = Person.objects.get(id=person_id)
        tree = Tree.objects.create(person_id=person_id)
        Visit.objects.create(purpose=1, tree=tree)
        
        html = render_to_string('people/person_list_item.html', {'person':person})
        
        return JsonResponse({'success':'Made list item', 'html':html})
     

#def create_planting_ajax(request):
#    if request.is_ajax():
#        id_list = request.GET.get('id_list')
#        ids = id_list.split(',')
        
#        for person_id in ids:
#            tree = Tree.objects.create(person_id=person_id)
#            Visit.objects.create(purpose=1, tree=tree)
    
#        return JsonResponse({'success': 'Created planting list for visit'})
        
        
def family_tree(request):
    person_id = request.GET.get('person_id', '1')
    person = Person.objects.get(id=person_id)
    children = Relationship.objects.filter(to_person=person, relationship=1).select_related('from_person')
    relationships = Relationship.objects.filter(from_person=person)
    rel_dict = {1:[], 2:[], 3:[]}
   
    for r in relationships:
        rel_dict[r.relationship]+=[r.to_person]
    #parents = [r for r in relationships if r.relationship == 1] # Relationship.objects.filter(from_person=person, relationship=1).select_related('to_person')
    #siblings = [r for r in relationships if r.relationship == 2] # Relationship.objects.filter(from_person=person, relationship=2).select_related('to_person')
    #spouse =  [r for r in relationships if r.relationship == 3] #Relationship.objects.filter(from_person=person, relationship=3).select_related('to_person')
    
    context = {
        'person': person,
        'parents': rel_dict[1],
        'siblings': rel_dict[2],
        'spouses': rel_dict[3],
        'children': children,
    }
    
    html = render_to_string('people/family_tree.html', context)
    
    return JsonResponse({'success':'Got family tree html', 'html':html})
    

def define_relationship_ajax(request, person_id):
    relationship = request.GET.get('relationship')
    relative_id = request.GET.get('relative_id')
    
    person = Person.objects.get(id=person_id)
    relative = Person.objects.get(id=relative_id)
    
    if relationship == '4':
        # Define person's child
        Relationship.objects.create(to_person=person, from_person=relative, relationship=1)
       
    else:
        Relationship.objects.get_or_create(from_person=person, to_person=relative, relationship=relationship)
        if not relationship == '1':
             Relationship.objects.get_or_create(to_person=person, from_person=relative, relationship=relationship)
             
    return JsonResponse({'success': 'Created relationship'})
    
    
    
def view_person(request):
    person_id = request.GET.get('person_id', 1)
    person = Person.objects.prefetch_related('trees').get(id=person_id)
    trees = person.trees.count()
    
    context = {
        'person': person,
        'trees': trees,
    }
    html = render_to_string('people/person_view.html', context)
    return JsonResponse({'success':'Got view person html', 'html':html})
    


def remove_tree_planting_ajax(request, person_id):
    person = Person.objects.get(id=person_id)
    tr = Tree.objects.filter(person_id=person_id, visit__purpose=1).first()
    print 'This tree', tr 
    print 'This visit', tr.visit_set.all()
    tr_id=tr.id
    tree = Tree.objects.filter(person_id=person_id, visit__purpose=1).first().delete()
    #Visit.objects.create(purpose=1, tree=tree)
    print Visit.objects.filter(tree__id=tr_id)
    
    return JsonResponse({'success': 'Deleted tree and visit'})
    
    
tree_report = TreeReport()


def reports(request):
    labels, stats = tree_report.get_death_stats()
    
    context = {
        'labels': labels,
        'stats': stats,
        
    }
    return render(request, '../templates/reports.html', context)
