from django.shortcuts import render
from django.template.loader import render_to_string

from .models import *
from .forms import MonitoringFormset, PlantingFormset

class Planting():
    def get_visits(self, purpose):
        return Visit.objects.prefetch_related('tree').filter(purpose=1)
        
    def get_context(self, purpose):
        if purpose in [1,'1']:
            visits = self.get_visits(purpose=purpose)
            formset = PlantingFormset(queryset=visits)
        else:
            formset = MonitoringFormset()
            
        context = {
            'visits': visits,
            'formset': formset
        }
        return context
        
    def get_form_html(self, purpose):
        html = render_to_string('trees/planting_data.html', self.get_context(purpose))
        return html

planting = Planting()

def enter_data(request, purpose):
    # If the user enters the loads the page on the website use this view #

    context = planting.get_context(purpose)
    return render(request, 'trees/planting_data.html', context)
    

class TreeReport():
    def get_death_reason_list(self):
        return [str(word) for i, word in dead_choices]
        
    def get_death_dic(self):
        # TO DO: Make this into a report and make other reports
        # Makes a dictionary of reasons that trees have died and the count
        trees = Visit.objects.filter(alive=False)
        death_dic = {word:trees.filter(reason_dead=i).count() for i, word in dead_choices}
        return death_dic
    
    def get_death_stats(self):
        death_dic = self.get_death_dic()
        labels = []
        stats = []
        for key in death_dic.keys():
            labels.append(str(key))
            stats.append(death_dic[key])
        return [labels, stats]