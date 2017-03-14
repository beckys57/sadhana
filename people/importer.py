from django.core.exceptions import MultipleObjectsReturned

from .models import *
from trees.models import *

import csv
from datetime import date

            
def save_date(date_str):
    date_split = date_str.split('.')
    if len(date_split) == 3:
        d,m,y = date_split
        if len(y) == 3:
            y = '20'+y
        if d and m and y:
           formatted_date = date(int(y), int(m), int(d))
        return formatted_date
    return

    
def make_coordinates(co_string):
    # Store coordinates:
    # gps_n = 8 digits, as xxNxxxxxx - make last digit 0 if missing
    # gps_e = 7 digits as x.xxxxxx - make last digit 0 if missing
    def make_length(coords, length):
        padded = coords + '000'
        return coords[:length]
    
    if co_string and co_string[2] == 'N':
        co_split = co_string.split(' ')
        if len(co_split) == 2:
            # Format is 37N0258969 0094507
            GPS_N = ''.join(co_split[0].split('N'))
            if co_split[1][:2] == '00':
                GPS_E = co_split[1][1:]
            else:
                GPS_E = co_split[1]
            return [GPS_N, GPS_E]
        elif len(co_split) == 3:
            # Format is 37N 0258969 0094507
            GPS_N = co_split[0][:2] + co_split[1][-6:]
            if co_split[2][:2] == '00':
                GPS_E = co_split[2][1:]
            elif co_split[2][0] == '0':
                GPS_E = co_split[2]
            else:
                print 'Co_split east not saving', co_split[2]
                return [GPS_N, '']
            return [make_length(GPS_N, 8), make_length(GPS_E, 7)]
    else:
        comma_split = co_string.split(',')
        if len(comma_split) == 2:
            if comma_split[0][0] == '0':
                GPS_E = comma_split[0]
                GPS_N = comma_split[1]
            elif comma_split[1][0] == '0':
                GPS_E = comma_split[1]
                GPS_N = comma_split[0]
            else:
                return False
            GPS_E = ''.join(GPS_E.split('.'))+'00'
            GPS_E = GPS_E[:7]
            GPS_N = ''.join(GPS_N.split('.'))+'00'
            GPS_E = GPS_E[:8]
            return [make_length(GPS_N, 8), make_length(GPS_E, 7)]
        else:
            # Check for false value and save coordinates in Tree.notes for manual sorting
            return False
    return False
    

def imp_trees(filename='people/trees.tsv'):
    species_list = TreeSpecies().get_species_list(active_only=False)
    #nengerpus_family = Family.objects.get_or_create(name='Nengerpus', village='Lekuru')[0]
    #pastor_j_family = Family.objects.get_or_create(name='Paston John', village='Lekuru')[0]
    causes_of_death = []
    mound_key = {word:i for i, word in mound_choices}
    trench_key = {word:i for i, word in trench_choices}
    dead_key = {word:i for i, word in dead_choices}
    
    with open(filename,'rb') as tsvin, open('new.csv', 'wb') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout)
    
        for row in tsvin:
            #PERSON
            #nengerpus = row[0][:9] == 'Nengerpus'
            #pastor_j = row[0][:13] == "Pastor John's"
            
            person_name = row[0].split(', ')
            if len(person_name) == 2:
                try:
                    person = Person.objects.get(first_name=person_name[1].strip(), last_name=person_name[0].strip())
                except MultipleObjectsReturned:
                    try:
                        person = Person.objects.get(first_name=person_name[1].strip(), last_name=person_name[0].strip(), village=row[4])
                    except:
                        'Multiple found, could not resolve with village'
                        continue
                except:
                    try:
                        person = Person.objects.get(first_name=person_name[1].strip(), phone=row[3])
                    except:
                        print 'person not found', person_name, row[5]
                        continue
            #elif nengerpus:
            #    person = Person.objects.get_or_create(first_name='Nengerpus', last_name='Primary School', family=nengerpus_family)[0]
            #elif pastor_j:
            #    person = Person.objects.get_or_create(first_name="Pastor John's", last_name='School, Lekuru', family=pastor_j_family)[0]
            else:
                person_name = row[0].split(' ')
                if 'SCHOOL' in row[0].upper():
                    school_name = row[0].split('School')
                    group = Family.objects.get_or_create(name='School')[0]
                    person = Person.objects.get_or_create(first_name=school_name[0].strip(), last_name='School', family=group)[0]
                elif 'CHURCH' in row[0].upper():
                    school_name = row[0].split('Church')
                    group = Family.objects.get_or_create(name='Church')[0]
                    person = Person.objects.get_or_create(first_name=school_name[0].strip(), last_name='Church', family=group)[0]
                elif len(person_name) == 2:
                    first_name = person_name[0]
                    if first_name[0] == '*':
                        first_name = first_name[1:]
                    try:
                        person = Person.objects.get(first_name=first_name.strip(), last_name=person_name[1].strip())
                    except:
                        print 'Bad name 2:', first_name, person_name[1], row[5]
                        continue
                else:
                    print 'Bad name:', person_name, row[5]
                    continue
                
            #FAMILY MOVES?
            if row[23] and row[23] != 'no':
                person.family.moves = True
                person.family.save()
            if row[24]:
                person.family.notes = row[24]
                person.family.save()
                
            
            tree = Tree(person=person, number=row[5])
            
            #COORDINATES
            coordinates = make_coordinates(row[6])
            if not coordinates:
                tree.notes = 'Coordinates: {}'.format(row[5])
            else:
                tree.gps_n = coordinates[0]
                tree.gps_e = coordinates[1]
            
            #SPECIES
            species = row[7]
            species_position = [i for i, x in enumerate(species_list) if x==species]
            if not species_position:
                species_list += [row[7]]
                tree.species = len(species_list)-1
            else:
                tree.species = species_position[0]
            
            #NOTES
            if row[10]:
                if tree.notes:
                    notes = tree.notes + row[10]
                    tree.notes = notes
                else:
                    tree.notes = row[10]
            #WATER
            if row[22]:
                water_details = row[22]
                split_details = water_details.split(',')
                if len(split_details) == 2:
                    seasonality = split_details[0]
                    if 'all year' in seasonality.lower():
                        tree.seasonality = False
                    water_distance = ''.join(split_details[1:]).strip()
                    if water_distance: tree.water_distance = water_distance
                    
            #SAVE
            tree.save()
            
            #PLANTING
            planting = Visit.objects.create(purpose=2, tree=tree)
            if row[8]:
                planting.date = save_date(row[8])
            if row[9]:
                try:
                    planting.height = int(''.join(row[9].split('cm')))
                except:
                    pass
            planting.save()
            
            
            #VISITS
            if row[12]:
                checkup = Visit(tree=tree, purpose=3, date=save_date(row[12]))
                #DEAD?
                if row[13] and 'DEAD' in row[13].upper():
                    checkup.alive = False
                    death = row[13].split('/')
                    if len(death) > 1:
                        death = death[1]
                        dead_index = dead_key.get(death)
                        if dead_index:
                            checkup.reason_dead = dead_index
                        elif death == 'migration':
                            checkup.reason_dead = 1
                        else:
                            print 'Dead', death
                            if death not in causes_of_death:
                                causes_of_death += [death]
                        
                #HEIGHT
                if row[14] not in ['', '-']:
                    try:
                        checkup.height = int(row[14].split('cm')[0])
                    except:
                        pass
                #DIAMETER   
                if row[15] not in ['', '-']:
                    try:
                        checkup.diameter = int(float(row[14].split('cm')[0])*10)
                    except:
                        pass
                #VITALITY
                if row[16]:
                    tree.vitality = row[16]
                #MOUND
                if row[17] not in ['', '-']:
                    mound = row[17].strip().lower()
                    mound_index = mound_key.get(mound)
                    if not mound_index == None:
                        tree.mound = mound_index
                    elif mound in ['intact', 'rebuilt']:
                        tree.mound = 4
                    else:
                        if mound in ['ok', 'eroded a bit', 'bit eroded', 'not bad']:
                            tree.mound = 3  
                        elif mound == 'poor':
                            tree.mound = 2
                        elif mound in ['little-nothing remaining', 'very very eroded', 'severly eroded', 'very poor', 'badly eroded', 'very eroded']:
                            tree.mound = 1                  
                        elif mound in ['none', 'no mound', 'gone']:
                            tree.mound = 0
                        else:
                            print 'Uncategorisable mound quality:', mound
                #FENCE
                if row[18] not in ['', '-']:
                    tree.fence = row[18]
                #TRENCH
                if row[19] not in ['', '-']:
                   trench = row[19].lower()
                   trench_index = trench_key.get(trench)
                   if not trench_index == None:
                       tree.trench = trench_index
                   else:
                        if trench == 'good':
                            tree.trench = 5
                        elif trench == 'ok':
                            tree.trench = 4
                        elif trench == 'small':
                            tree.trench = 3
                        elif trench in ['1/2 full', 'half empty', 'poor']:
                            tree.trench = 2
                        elif trench in ['very poor', 'almost full', 'mostly full']:
                            tree.trench = 1
                        elif trench in ['none', 'gone']:
                            tree.trench = 0
                        else:
                            print 'Uncategorisable trench quality:', trench
                #IRRIGATED
                if row[21] == 'no':
                    checkup.irrigated = False
                checkup.save()
                
    if row[5]:
        try:
            if int(row[5]) > 760: print 'Causes of death', causes_of_death
        except:
            pass
                  
            
            
filename='people/people.tsv'
def imp(filename='people/people.tsv'):
    with open(filename,'rb') as tsvin, open('new.csv', 'wb') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout)
    
        for row in tsvin:
            family = Family.objects.create(name=row[0])
            peep = Person(family=family, last_name=row[0].strip(), first_name=row[1].strip(), village=row[3], phone=row[4])
            
            # Gender
            if row[2]:
                gender = row[2].lower()
                if gender == 'f': peep.gender = True
                
            # Training dates

                    
            if row[5]:
                peep.training_date = save_date(row[5])
            if row[7]:
                peep.training_date_w = save_date(row[7])
            if row[8]:
                peep.mapping_date = save_date(row[8])
            if row[9]:
                peep.nrm_date = save_date(row[9])
            
            if row[10]:
                peep.tours = row[10]
            if row[11]:
                peep.training_other = row[11]
            if row[12]:
                peep.notes = row[12]
                
                
            peep.save()
            
        	#Water Conservation Training	Resource Mapping	NRM Planning	Demos/Tour	Other Outreach/Trainings	Comments