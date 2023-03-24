from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from .forms import AnimalClassForm, AnimalNurturingForm, AnimalLegsForm          # import forms

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
    
    return render(request, 'configs.html')

def queries(request):
    """Renders the queries page."""
    assert isinstance(request, HttpRequest)

    animal_class_form = AnimalClassForm(request.POST)
    animal_nurturing_form = AnimalNurturingForm(request.POST)
    animal_legs_form = AnimalLegsForm(request.POST)

    #print(request.POST)

    # user selected an animal class
    if 'animal_class' in request.POST:
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
            request.session['animal_list'].append(e['animal_name']['value'])

        return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': animal_class_form, 'animal_nurturing_form': AnimalNurturingForm(), 'animal_legs_form': AnimalLegsForm() })
    
    # user select an animal nurturing
    elif 'animal_nurturing' in request.POST:
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
            request.session['animal_list'].append(e['animal_name']['value'])

        return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': animal_nurturing_form, 'animal_legs_form': AnimalLegsForm() })

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
            request.session['animal_list'].append(e['animal_name']['value'])

        return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': AnimalNurturingForm() , 'animal_legs_form': animal_legs_form })
    
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
        
        query = query.replace("_animal_name", request.POST['animal_item'])

        payload_query = { "query": query }
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)

        res = json.loads(res)

        description = []
        for e in res['results']['bindings']:
            #print(e['animal_id']['value'])
            #print(e['p']['value'])
            #print(e['o']['value'])

            key = e['p']['value'].split("/")[-1]

            print(key)

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
    else:
        request.session['animal_list'] = []
        request.session['animal_description'] = {}

    return render(request, 'queries.html', { 'session': request.session, 'animal_class_form': AnimalClassForm(), 'animal_nurturing_form': AnimalNurturingForm(), 'animal_legs_form': AnimalLegsForm() })

def ask(request):
    """Renders the ask page."""
    assert isinstance(request, HttpRequest)
    
    return render(request, 'ask.html')