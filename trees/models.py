from __future__ import unicode_literals

from django.db import models
from people.models import Person


class TreeSpecies():
    # Reads the file containing species, separated by new lines
    # Species prefixed with a * are excluded by the get_active method
    
    def get_species_list(self, active_only):
        species_file = open('trees/species_list.txt')
        species_list = species_file.read().splitlines()
        if active_only:
            # Only includes those which have been added correctly (denoted by absence of * at start of line)
            return [sp for sp in species_list if not sp[0]=='*']
        else:
            # Includes those which might have been added by mistake, duplicates etc.
            return species_list
        
    def get_choices(self, active_only=False):
        species_list = self.get_species_list(active_only)
        return [(i, species) for i, species in enumerate(species_list)]

        
species = TreeSpecies()
        
        
class Tree(models.Model):
    person = models.ForeignKey(Person, related_name='trees')
    species = models.PositiveSmallIntegerField(choices=species.get_choices(active_only=False), default=1)
    gps_n = models.CharField(null=True, blank=True, max_length=15) # GPS N coordinate
    gps_e = models.CharField(null=True, blank=True, max_length=15) # GPS E coordinate
    caretaker = models.CharField(null=True, blank=True, max_length=60)
    water_seasonality = models.BooleanField(default=True)
    water_distance = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    number = models.PositiveSmallIntegerField(null=True, blank=True) # From the old spreadsheet
    
visit_choices = [
    (1, 'Pending'), # In progress
    (2, 'Planting'),
    (3, 'Monitoring'),
    ]
    
dead_choices = [
     (1, 'moved'),
     (2, 'animals'),
     (3, 'children'),
     (4, 'termites'),
     (5, 'salt'),
     (6, 'dryness'),
     (7, 'no water'),
     (8, 'dry'),
     (9, 'conflict'),
     (10, 'syz'),
 ]
    

mound_choices = [
    (0, 'gone'), # Also used for none
    (1, 'severely eroded'),
    (2, 'eroded'),
    (3, 'partially eroded'),
    (4, 'good'),
    ]
    
trench_choices = [
    (0, 'full'), # Also used for none
    (1, 'nearly full'),
    (2, 'half full'),
    (3, 'small'),
    (4, 'silted'),
    (5, 'empty'),
    ]
    
class Visit(models.Model):
    tree = models.ForeignKey(Tree, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    purpose = models.PositiveSmallIntegerField(default=1, choices=visit_choices)
    notes = models.TextField(null=True, blank=True)
    alive = models.BooleanField(default=True)
    reason_dead = models.PositiveSmallIntegerField(null=True, blank=True, choices=dead_choices)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    diameter = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='root crown diameter')
    vitality = models.CharField(max_length=100, null=True, blank=True)
    mound = models.PositiveSmallIntegerField(null=True, blank=True, choices=mound_choices, verbose_name='mound quality')
    fence = models.CharField(null=True, blank=True, max_length=140, verbose_name='fence quality')
    trench = models.PositiveSmallIntegerField(null=True, blank=True, choices=mound_choices, verbose_name='trench quality')
    irrigated = models.BooleanField(default=True, verbose_name='bottle irrigation clear?')
    