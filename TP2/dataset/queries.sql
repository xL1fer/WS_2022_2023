-- Land animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
construct {
   ?s a animalc:Animal .
}
where {
    ?s a animalc:Animal .
    filter NOT EXISTS { ?s zoop:Has "Fins". } .
}


-- Aracnid animals
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX animalc: <http://zoo.org/class/>
PREFIX zoop: <http://zoo.org/pred/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
construct {
   ?s a animalc:Arachnid .
}
where {
    {
        ?s zoop:class ?classid .
        ?classid zoop:name "Insect" .
	}
    union
    {
        ?s zoop:class ?classid .
        ?classid zoop:name "Invertebrate" .
    }
}