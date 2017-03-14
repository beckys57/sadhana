from __future__ import unicode_literals

from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=30)
    village = models.CharField(null=True, blank=True, max_length=30)
    moves = models.BooleanField(default=False, verbose_name='moves in dry season')
    notes = models.TextField(null=True, blank=True, verbose_name='level of engagement with SFK')
    
    def total_trees(self):
        family_members = self.members.all()
        # Do an annotate with Count to get the trees
        return 1234321
        
        #/ TO DO: delete empty families
    
def get_relationship_choices():
    return [
        (1, 'Parent'),
        (2, 'Sibling'),
        (3, 'Spouse'),
        ]
    
class Relationship(models.Model):
    from_person = models.ForeignKey('Person', related_name='from_people') # Child
    to_person = models.ForeignKey('Person', related_name='to_people') # Parent
    relationship = models.PositiveSmallIntegerField(choices=get_relationship_choices())
    
    def add_relationship(self, person, relationship):
        relationship, created = Relationship.objects.get_or_create(
        from_person=self,
        to_person=person,
        relationship=relationship)
        return relationship

    def remove_relationship(self, person, relationship):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            relationship=relationship).delete()
        return
    
def get_flag_choices():
    return [
        (1, 'Red'),
        (2, 'Green'),
        (3, 'Blue'),
        ]
    
class Person(models.Model):
    family = models.ForeignKey(Family, related_name='members')
    relative = models.ManyToManyField('Person', through=Relationship, symmetrical=False, related_name='relatives')
    head_of_family = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    gender = models.BooleanField(default=False) # True = F // False = M
    village = models.CharField(null=True, blank=True, max_length=30)
    phone = models.CharField(null=True, blank=True, max_length=30)
    
    
    training_date = models.DateField(null=True, blank=True)
    training_date_w = models.DateField(null=True, blank=True, verbose_name='water conservation training')
    mapping_date = models.DateField(null=True, blank=True, verbose_name='resource mapping')
    nrm_date = models.DateField(null=True, blank=True, verbose_name='NRM mapping')
    demos = models.CharField(null=True, blank=True, max_length=100)
    training_other = models.CharField(null=True, blank=True, max_length=100)
    
    notes = models.TextField(null=True, blank=True)
    flag = models.PositiveSmallIntegerField(null=True, blank=True, choices=get_flag_choices())
    
    class Meta:
        ordering = ['last_name']
        
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
