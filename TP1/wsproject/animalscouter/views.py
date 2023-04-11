from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime

from .forms import AnimalClassForm, AnimalNurturingForm, AnimalLegsForm, AnimalAskForm, InsertAnimalForm, DeleteAnimalForm    # import forms

"""
    GraphDB related imports and initializations
"""
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "zoo"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

"""
    Application views
"""

def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    return render(request, 'index.html')

def configs(request):
    """Renders the configs page."""
    assert isinstance(request, HttpRequest)

    insert_animal_form = InsertAnimalForm(request.POST)
    delete_animal_form = DeleteAnimalForm(request.POST)
    print(request.POST)

    # insert animal
    if 'insert_animal_name' in request.POST:
        if request.POST['animal_class'] == '-1' or request.POST['animal_legs'] == '-1':
            insert_response = 'Error: class and legs fields must be chosen'

            return render(request, 'configs.html', { 'session': request.session, 'insert_animal_form': insert_animal_form, 'delete_animal_form': delete_animal_form, 'insert_response': insert_response })
                
        update = """
                base <http://zoo.org/>
                prefix id: <http://zoo.org/animal/id/>
                prefix pred: <http://zoo.org/pred/>
                prefix class: <http://zoo.org/class/id/>
                prefix nurt: <http://zoo.org/nurt/id/>
                insert data {
                    id:_name_id pred:name "_animal_name".
                    id:_name_id pred:class class:_class_id.
                """

        name_id = request.POST['insert_animal_name']
        name_id = name_id.replace(" ", "_").lower()

        if 'animal_domestic' in request.POST:
            update += """id:_name_id pred:is "Domestic".\n"""
        if 'animal_toothed' in request.POST:
            update += """id:_name_id pred:is "Toothed".\n"""
        if 'animal_venomous' in request.POST:
            update += """id:_name_id pred:is "Venomous".\n"""
        if 'animal_aquatic' in request.POST:
            update += """id:_name_id pred:is "Aquatic".\n"""
        if 'animal_airborne' in request.POST:
            update += """id:_name_id pred:is "Airborne".\n"""
        if 'animal_milk' in request.POST:
            update += """id:_name_id pred:nurt nurt:2.\n"""
        if 'animal_eggs' in request.POST:
            update += """id:_name_id pred:nurt nurt:1.\n"""
        if 'animal_tail' in request.POST:
            update += """id:_name_id pred:has "Tail".\n"""
        if 'animal_fins' in request.POST:
            update += """id:_name_id pred:has "Fins".\n"""
        if 'animal_feathers' in request.POST:
            update += """id:_name_id pred:has "Feathers".\n"""
        if 'animal_hair' in request.POST:
            update += """id:_name_id pred:has "Hair".\n"""
        if 'animal_legs' in request.POST and request.POST['animal_legs'] != '0':
            update += """id:_name_id pred:legs "%s".\n""" % request.POST['animal_legs']

        update += "}"

        update = update.replace("_name_id", name_id)
        update = update.replace("_animal_name", request.POST['insert_animal_name'].title())
        update = update.replace("_class_id", request.POST['animal_class'])

        #print(update)

        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

        insert_response = 'Animal "' + request.POST['insert_animal_name'].title() + '" inserted'

        return render(request, 'configs.html', { 'session': request.session, 'insert_animal_form': InsertAnimalForm(), 'delete_animal_form': DeleteAnimalForm(), 'insert_response': insert_response })

    # delete animal
    if 'delete_animal_name' in request.POST:
        update = """
                base <http://zoo.org/>
                prefix pred: <http://zoo.org/pred/>
                delete { ?s ?p ?o }
                where {
                    ?s pred:name "_animal_name".
                    ?s ?p ?o.
                }
                """
        update = update.replace("_animal_name", request.POST['delete_animal_name'].title())

        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

        delete_response = 'Animal "' + request.POST['delete_animal_name'].title() + '" deleted'

        return render(request, 'configs.html', { 'session': request.session, 'insert_animal_form': InsertAnimalForm(), 'delete_animal_form': DeleteAnimalForm(), 'delete_response': delete_response })

    return render(request, 'configs.html', { 'session': request.session, 'insert_animal_form': InsertAnimalForm(), 'delete_animal_form': DeleteAnimalForm() })

def queries(request):
    """Renders the queries page."""
    assert isinstance(request, HttpRequest)

    animal_class_form = AnimalClassForm(request.POST)
    animal_nurturing_form = AnimalNurturingForm(request.POST)
    animal_legs_form = AnimalLegsForm(request.POST)

    print(request.POST)

    # searching for animals by class
    if 'animal_class' in request.POST:
        class_dict = { '1': 'Mammal',
                     '2': 'Bird',
                     '3': 'Reptile',
                     '4': 'Fish',
                     '5': 'Amphibian',
                     '6': 'Insect',
                     '7': 'Invertebrate',
                    }
        query = """
                base <http://zoo.org/>
                prefix pred: <http://zoo.org/pred/>
                prefix class: <http://zoo.org/class/id/>
                select ?class_name ?animal_name
                where {
                    class:_class_id pred:name ?class_name.
                    ?animal_id pred:class class:_class_id.
                    ?animal_id pred:name ?animal_name.
                }
                """
        
        query = query.replace("_class_id", request.POST['animal_class'])

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        request.session['animal_list'] = []
        request.session['animal_description'] = {}
        for e in res['results']['bindings']:
            request.session['animal_list'].append((e['animal_name']['value'].replace(" ", "_"), e['animal_name']['value']))

        scout_description = '"Class ' + class_dict[request.POST['animal_class']] + '"'

        return render(request, 'queries.html', { 'session': request.session, 'scout_description': scout_description, 'animal_class_form': animal_class_form, 'animal_nurturing_form': AnimalNurturingForm(), 'animal_legs_form': AnimalLegsForm() })
    
    # searching for animals by nurturing
    elif 'animal_nurturing' in request.POST:
        nurt_dict = { '1': 'Eggs',
                     '2': 'Milk',
                     '3': 'Both'
                    }

        query = """"""
        
        if int(request.POST['animal_nurturing']) < 3:
            query = """
                    base <http://zoo.org/>
                    prefix pred: <http://zoo.org/pred/>
                    prefix nurt: <http://zoo.org/nurt/id/>
                    select ?nurt_name ?animal_name
                    where {
                        nurt:_nurt_id pred:name ?nurt_name.
                        ?animal_id pred:nurt nurt:_nurt_id.
                        ?animal_id pred:name ?animal_name.
                    }
                    """
            
            query = query.replace("_nurt_id", request.POST['animal_nurturing'])
        
        else:
            query = """
                    base <http://zoo.org/>
                    prefix pred: <http://zoo.org/pred/>
                    prefix nurt: <http://zoo.org/nurt/id/>
                    select ?animal_name
                    where {
                        {
                            ?animal_id pred:nurt nurt:1.
                            ?animal_id pred:name ?animal_name.
                        }
                        {
                            ?animal_id pred:nurt nurt:2.
                            ?animal_id pred:name ?animal_name.
                        }
                    }
                    """
            
            query = query.replace("_nurt_id", request.POST['animal_nurturing'])

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        request.session['animal_list'] = []
        request.session['animal_description'] = {}
        for e in res['results']['bindings']:
            request.session['animal_list'].append((e['animal_name']['value'].replace(" ", "_"), e['animal_name']['value']))

        scout_description = '"Nurturing ' + nurt_dict[request.POST['animal_nurturing']] + '"'

        return render(request, 'queries.html', { 'session': request.session, 'scout_description': scout_description, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': animal_nurturing_form, 'animal_legs_form': AnimalLegsForm() })
    
    # searching for animals by number of legs
    elif 'animal_legs' in request.POST:
        query = """"""

        if int(request.POST['animal_legs']) > 0:
            query = """
                    base <http://zoo.org/>
                    prefix pred: <http://zoo.org/pred/>
                    prefix class: <http://zoo.org/class/id/>
                    select ?animal_name
                    where {
                        ?animal_id pred:legs ?legs_number.
                        ?animal_id pred:name ?animal_name.
                        filter(?legs_number = "_legs_number").
                    }
                    """
        else:
            query = """
                    base <http://zoo.org/>
                    prefix pred: <http://zoo.org/pred/>
                    prefix class: <http://zoo.org/class/id/>
                    select ?animal_name
                    where {
                        ?animal_id pred:name ?animal_name.
                        filter NOT EXISTS { ?animal_id pred:legs ?legs_number. }.
                        filter EXISTS { ?animal_id pred:class ?class_name. }.
                    }
                    """
            
        query = query.replace("_legs_number", request.POST['animal_legs'])

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        request.session['animal_list'] = []
        request.session['animal_description'] = {}
        for e in res['results']['bindings']:
            request.session['animal_list'].append((e['animal_name']['value'].replace(" ", "_"), e['animal_name']['value']))

        scout_description = '"' + request.POST['animal_legs'] + ' Legs"'

        return render(request, 'queries.html', { 'session': request.session, 'scout_description': scout_description, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': AnimalNurturingForm() , 'animal_legs_form': animal_legs_form })
    
    # searching for all the characteristics of a specific animal
    elif 'animal_item' in request.POST:
        query = """
                base <http://zoo.org/>
                prefix pred: <http://zoo.org/pred/>
                prefix class: <http://zoo.org/class/id/>
                select ?animal_id ?p ?o
                where {
                    ?animal_id pred:name "_animal_name".
                    ?animal_id ?p ?o.
                }
                """
        
        query = query.replace("_animal_name", request.POST['animal_item'].replace("_", " "))

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        description = []
        for e in res['results']['bindings']:
            #print(e['animal_id']['value'])
            #print(e['p']['value'])
            #print(e['o']['value'])

            key = e['p']['value'].split("/")[-1]

            #print(key)

            if key == "class":
                class_query = """
                        base <http://zoo.org/>
                        prefix pred: <http://zoo.org/pred/>
                        prefix class: <http://zoo.org/class/id/>
                        select ?class_name
                        where {
                            class:_class_id pred:name ?class_name.
                        }
                        """
                
                class_query = class_query.replace("_class_id", e['o']['value'].split("/")[-1])

                payload_query = { "query": class_query }
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

                res = json.loads(res)

                for e in res['results']['bindings']:
                    value = e['class_name']['value'].lower()

            elif key == "nurt":
                nurt_query = """
                        base <http://zoo.org/>
                        prefix pred: <http://zoo.org/pred/>
                        prefix nurt: <http://zoo.org/nurt/id/>
                        select ?nurt_name
                        where {
                            nurt:_nurt_id pred:name ?nurt_name.
                        }
                        """
                
                nurt_query = nurt_query.replace("_nurt_id", e['o']['value'].split("/")[-1])

                payload_query = { "query": nurt_query }
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

                res = json.loads(res)

                for e in res['results']['bindings']:
                    value = e['nurt_name']['value'].lower()

            else:
                value = e['o']['value'].lower()

            description.append((key.title(), value.title()))

        request.session['animal_description'] = description

        return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': animal_class_form, 'animal_nurturing_form': animal_nurturing_form, 'animal_legs_form': animal_legs_form })
    
    # searching for animals with a same specific characteristic as the scouted animal
    elif 'Name' in request.POST or 'Class' in request.POST or 'Legs' in request.POST or 'Nurt' in request.POST or 'Has' in request.POST or 'Is' in request.POST:
        obj_dict = { 'Mammal': '<http://zoo.org/class/id/1>',
                    'Bird': '<http://zoo.org/class/id/2>',
                    'Reptile': '<http://zoo.org/class/id/3>',
                    'Fish': '<http://zoo.org/class/id/4>',
                    'Amphibian': '<http://zoo.org/class/id/5>',
                    'Insect': '<http://zoo.org/class/id/6>',
                    'Invertebrate': '<http://zoo.org/class/id/7>',
                    'Eggs': '<http://zoo.org/nurt/id/1>',
                    'Milk': '<http://zoo.org/nurt/id/2>'
                    }
        
        query = """
                base <http://zoo.org/>
                prefix pred: <http://zoo.org/pred/>
                prefix class: <http://zoo.org/class/id/>
                select ?animal_name
                where {
                    ?animal_id pred:_pred_name _obj_name.
                    ?animal_id pred:name ?animal_name.
                }
                """
        
        pred = list(request.POST.keys())[1]
        obj = ''

        if pred == 'Class' or pred == 'Nurt':
            obj += obj_dict[request.POST[pred]]
        else:
            obj += '"' + request.POST[pred] + '"'

        query = query.replace("_pred_name", pred.lower())
        query = query.replace("_obj_name", obj)

        #print(query)

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        request.session['animal_list'] = []
        request.session['animal_description'] = {}
        for e in res['results']['bindings']:
            request.session['animal_list'].append((e['animal_name']['value'].replace(" ", "_"), e['animal_name']['value']))

        if pred == 'Legs':
            scout_description = '"'+ request.POST[pred] + ' ' + pred + '"'
        else:
            scout_description = '"'+ pred + ' ' + request.POST[pred] + '"'

        return render(request, 'queries.html', { 'session': request.session, 'scout_description': scout_description, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': AnimalNurturingForm(), 'animal_legs_form': AnimalLegsForm() })
    
    # reset all forms
    else:
        request.session['animal_list'] = []
        request.session['animal_description'] = {}

    return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': AnimalNurturingForm(), 'animal_legs_form': AnimalLegsForm() })

def ask(request):
    """Renders the ask page."""
    assert isinstance(request, HttpRequest)

    animal_ask_form = AnimalAskForm(request.POST)

    #print(request.POST)

    if 'animal_question' in request.POST:
        query = """
                base <http://zoo.org/>
                prefix pred: <http://zoo.org/pred/>
                ask { 
                    ?animal_s pred:name "_animal_name".
                    ?animal_s pred:_pred "_animal_attribute".
                }
                """
        
        animal_question = request.POST['animal_question']
        
        query = query.replace("_animal_name", request.POST['animal_name'].lower().title())
        query = query.replace("_pred", animal_question.split("_")[0])
        query = query.replace("_animal_attribute", animal_question.split("_")[1].title())

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        return render(request, 'ask.html', { 'ask_response': res['boolean'], 'animal_ask_form': animal_ask_form })

    return render(request, 'ask.html', { 'animal_ask_form': animal_ask_form })