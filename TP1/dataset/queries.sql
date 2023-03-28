-- get all animals from a given class

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix class: <http://zoo.org/class/id/>
select ?class_name ?animal_name
where {
    class:3 pred:name ?class_name.
	?animal_id pred:class class:3.
    ?animal_id pred:name ?animal_name.
}

-- get all animals that produce a given nurturing

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix nurt: <http://zoo.org/nurt/id/>
select ?nurt_name ?animal_name
where {
    nurt:1 pred:name ?nurt_name.
	?animal_id pred:nurt nurt:1.
    ?animal_id pred:name ?animal_name.
}

-- select all animals that produce milk or eggs

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix nurt: <http://zoo.org/nurt/id/>
SELECT ?animal_name
WHERE {
	{
		nurt:1 pred:name ?nurt_name.
		?animal_id pred:nurt nurt:1.
		?animal_id pred:name ?animal_name.
	}
	{
		nurt:2 pred:name ?nurt_name.
		?animal_id pred:nurt nurt:2.
		?animal_id pred:name ?animal_name.
	}
}

-- select all animals that have a certain amount of legs

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix class: <http://zoo.org/class/id/>
select ?animal_name
where {
	?animal_id pred:legs ?legs_number.
	?animal_id pred:name ?animal_name.
	filter(?legs_number = "8").
}

-- select all animal properties given its name

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix class: <http://zoo.org/class/id/>
select ?animal_id ?p ?o
where {
    ?animal_id pred:name "Spider".
    ?animal_id ?p ?o.
}

-- select class name based on class id

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix class: <http://zoo.org/class/id/>
select ?class_name
where {
    class:1 pred:name ?class_name.
}

-- select nurt name based on nurt id

base <http://zoo.org/>
prefix pred: <http://zoo.org/pred/>
prefix nurt: <http://zoo.org/nurt/id/>
select ?nurt_name
where {
	nurt:1 pred:name ?nurt_name.
}



/**********************************************/



	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	select ?animal_name
	where {
		?animal_id pred:class class:_class_id.
		?animal_id pred:name ?animal_name.
	}

	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix nurt: <http://zoo.org/nurt/id/>
	select ?animal_name
	where {
		?animal_id pred:nurt nurt:_nurt_id.
		?animal_id pred:name ?animal_name.
	}
	
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
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	select ?animal_name
	where {
		?animal_id pred:legs ?legs_number.
		?animal_id pred:name ?animal_name.
		filter(?legs_number = "_legs_number").
	}
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	select ?animal_name
	where {
		?animal_id pred:name ?animal_name.
		filter NOT EXISTS { ?animal_id pred:legs ?legs_number. }.
		filter EXISTS { ?animal_id pred:class ?class_name. }.
	}
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	select ?animal_id ?p ?o
	where {
		?animal_id pred:name "_animal_name".
		?animal_id ?p ?o.
	}
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	select ?class_name
	where {
		class:_class_id pred:name ?class_name.
	}
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	prefix nurt: <http://zoo.org/nurt/id/>
	select ?nurt_name
	where {
		nurt:_nurt_id pred:name ?nurt_name.
	}
	
	
	
	
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	ask { 
		?animal_s pred:name "_animal_name".
		?animal_s pred:_pred "_animal_attribute".
	}
	
	
	
	
	
	base <http://zoo.org/>
	prefix id: <http://zoo.org/animal/id/>
	prefix pred: <http://zoo.org/pred/>
	prefix class: <http://zoo.org/class/id/>
	prefix nurt: <http://zoo.org/nurt/id/>
	insert data {
		id:_name_id pred:name "_animal_name".
		id:_name_id pred:class class:_class_id.
		id:_name_id pred:is "Domestic".
		id:_name_id pred:is "Airborne".
		id:_name_id pred:nurt nurt:1.
		id:_name_id pred:has "Feathers".
		# (...)
	}
	
	base <http://zoo.org/>
	prefix pred: <http://zoo.org/pred/>
	delete { ?s ?p ?o }
	where {
		?s pred:name "_animal_name".
		?s ?p ?o.
	}
	
	
	