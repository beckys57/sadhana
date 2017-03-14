from django.shortcuts import render

from .models import *
from .forms import MonitoringFormset, PlantingFormset

def enter_data(request, purpose):
    if purpose in [1,'1']:
        visits = Visit.objects.prefetch_related('tree').filter(purpose=1)
        formset = PlantingFormset(queryset=visits)
    else:
        formset = MonitoringFormset()
        
    context = {
        'visits': visits,
        'formset': formset
    }
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