from django.forms import modelformset_factory
from django import forms

from .models import Tree, Visit


#class MonitoringForm(forms.ModelForm):
#    class Meta:
#        model = Tree
#        exclude = ['caretaker']
        
PlantingFormset = modelformset_factory(model=Tree, extra=0, exclude=['caretaker'])

MonitoringFormset = modelformset_factory(model=Visit, extra=0, exclude=['tree'])