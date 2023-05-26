# Animal Scouter
Master's in Computer Engineering's first project under the course of Web Semantics at the University of Aveiro.

# Setup

## Requirements
Installation requirements to set the developed application up and running:

    •	Python (preferably 3.8.10 or higher)
    •	GraphDB
    •	s4api (pip install s4api)
	•	sparqlwrapper (pip install sparqlwrapper)

## Creating the database
In GrapDB control panel, it is needed to create a database named “zoo” with ruleset OWL2-RL and import the provided “zooall.n3” N3 file.
Optionally, for the base url, http://zoo.org/ may be used.

## Running with PyCharm
To run the application with PyCharm, simply open the wsproject folder and press the run button. Then, a localhost link should appear in the console which needs to be opened with a web browser.

## Running with command line
For running the application using the command line, open a new command line in the “/wsproject/” directory and type the command “py manage.py runserver”. A localhost link should appear in the console which needs to be opened with a web browser.
