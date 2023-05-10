-- Bird animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
   ?s a animalc:Bird.
}
WHERE {
    ?s a animalc:Animal.
    ?s zoop:has "Feathers".
}


PREFIX animalc: <http://zoo.org/class/>
select ?s
WHERE {
	?s a animalc:Bird.
}


-- Land animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
	?s a animalc:Land.
}
WHERE {
    ?s a animalc:Animal.
	filter NOT EXISTS { ?s zoop:is "Airborne". }.
	filter NOT EXISTS { ?s zoop:is "Aquatic". }.
}


PREFIX animalc: <http://zoo.org/class/>
SELECT ?s
WHERE {
	?s a animalc:Land.
}


-- Mammal animals
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX zoon: <http://zoo.org/nurt/id/>
CONSTRUCT {
	?s a animalc:Mammal.
}
WHERE {
	OPTIONAL {
		?s zoop:has "Hair".
	}
	?s zoop:nurt zoon:2.
	?s zoop:has "Backbone".
}


PREFIX animalc: <http://zoo.org/class/>
SELECT ?s
WHERE {
	?s a animalc:Mammal.
}


-- Fish animals
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX zoon: <http://zoo.org/nurt/id/>
CONSTRUCT {
	?s a animalc:Fish.
}
WHERE {
	?s zoop:has "Fins".
    ?s zoop:nurt zoon:1.
}










-- Insect animals
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
	?s a animalc:Insect.
}
WHERE {
	?s zoop:legs "6".
	?s zoop:nurt nurt:1.
}


-- Arachnid animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
CONSTRUCT {
   ?s a animalc:Arachnid.
}
WHERE {
    {
        ?s zoop:class ?classid.
        ?classid zoop:name "Insect".
	}
    UNION
    {
        ?s zoop:class ?classid.
        ?classid zoop:name "Invertebrate".
    }
}