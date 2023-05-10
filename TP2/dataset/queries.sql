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


-- Arthropod animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
CONSTRUCT {
   ?s a animalc:Arthropod.
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


-- Reptilia animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
CONSTRUCT {
   ?s a animalc:Reptilia.
}
WHERE {
    {
        ?s zoop:class ?classid.
        ?classid zoop:name "Amphibian".
	}
    UNION
    {
        ?s zoop:class ?classid.
        ?classid zoop:name "Reptile".
    }
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