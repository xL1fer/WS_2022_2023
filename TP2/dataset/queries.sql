-- Arthropod animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
CONSTRUCT {
   ?s a animalc:Arthropod.
}
WHERE {
	?s zoop:class ?classid.
	?classid zoop:name "Insect".
}


-- Warm-Blood animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
   ?s a animalc:Warm-Blood.
}
WHERE {
	{
		?s a animalc:Animal.
		?s zoop:has "Feathers".
	}
	UNION
	{
		OPTIONAL {
			?s zoop:has "Hair".
		}
		?s zoop:nurt zoon:2.
		?s zoop:has "Backbone".
	}
}


-- Cold-Blood animals
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX zoon: <http://zoo.org/nurt/id/>
CONSTRUCT {
	?s a animalc:Cold-Blood.
}
WHERE {
	?s zoop:has "Fins".
    ?s zoop:nurt zoon:1.
	UNION
	{
		?s zoop:class ?classid.
		?classid zoop:name "Reptile".
	}
	UNION
	{
		?s zoop:class ?classid.
		?classid zoop:name "Amphibian".
	}
}


-- Backbone animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
   ?s a animalc:Backbone.
}
WHERE {
	{
		?s a animalc:Animal.
		?s zoop:has "Feathers".
	}
	UNION
	{
		OPTIONAL {
			?s zoop:has "Hair".
		}
		?s zoop:nurt zoon:2.
		?s zoop:has "Backbone".
	}
	UNION
	{
		?s zoop:has "Fins".
		?s zoop:nurt zoon:1.
	}
	UNION
	{
		?s zoop:class ?classid.
		?classid zoop:name "Reptile".
	}
	UNION
	{
		?s zoop:class ?classid.
		?classid zoop:name "Amphibian".
	}
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


-- No-Backbone animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
CONSTRUCT {
   ?s a animalc:No-Backbone.
}
WHERE {
    ?s a animalc:Animal.
	filter NOT EXISTS { ?s zoop:has "Backbone". }.
}


-- Mammal animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX zooc: <http://zoo.org/class/id/>
CONSTRUCT {
   ?s a animalc:Mammal.
}
WHERE {
    ?s a animalc:Animal.
	?s zoop:class zooc:1.
}



Animals


Backbone																No-Backbone


Warm-Blood				Cold-Blood										Arthropod


Mammal		Bird		Fish		Reptile		Amphibian				Insect			Invertebrate