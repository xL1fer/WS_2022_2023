"""
    parsedata.py

    ====================================

    University of Aveiro
    Department of Electronics, Telecommunications and Informatics

    Web Semantics
    Master's in Computer Engineering

    João Bernardo Coelho Leite - 115041
    João Pedro dos Reis - 115513
    Luís Miguel Gomes Batista - 115279

    ====================================
    
    1st Project
    Dataset parser
"""

import csv

base_URI = '<http://zoo.org/'

animal_id_URI = 'animal/id/'
class_id_URI = 'class/id/'
nurt_id_URI = 'nurt/id/'

name_pred_URI = 'pred/name'
class_pred_URI = 'pred/class'
nurt_pred_URI = 'pred/nurt'
legs_pred_URI = 'pred/legs'
has_pred_URI = 'pred/has'
is_pred_URI = 'pred/is'

class_list = { 1: '"Mammal"', 2: '"Bird"', 3: '"Reptile"', 4: '"Fish"', 5: '"Amphibian"', 6: '"Insect"', 7: '"Invertebrate"' }
nurturing_list = { 1: '"Eggs"', 2:'"Milk"' }

def main(args):
    """
        Main function

        Parameters
        ----------
        args
            arguments passed through command line
        Returns
        ----------
        0
            program exits normally
        other than 0
            program fails to completely run
    """
    dataset = load("zoo.csv")
    nt = generate_NT(dataset)

    save_NT(nt)
    
    return 0

def load(filename):
    """
        Load a csv dataset file

        Parameters
        ----------
        filename
            name of the file to be loaded
        Returns
        ----------
        dataset
            loaded dataset
    """
    f = open(filename, 'r', encoding='utf-8')
    dataset = list(csv.reader(f))
    f.close()

    return dataset

def generate_NT(dataset):
    """
        Generate a N-Triples version of the given zoo dataset

        Parameters
        ----------
        dataset
            dataset file loaded list
        Returns
        ----------
        nt
            N-Triples dataset conversion
    """
    nt = []

    extract_class(nt)
    extract_nurturing(nt)
    
    extract_animals(nt, dataset)
    #print(data)

    return nt

def extract_class(nt):
    """
        Extract class to N-Triples list

        Parameters
        ----------
        nt
            N-Triples dataset
    """
    for key, value in class_list.items():
        # (class_id pred_class class_name)
        temp = base_URI + class_id_URI + str(key) + '> '
        temp += base_URI + name_pred_URI + '> '
        temp += value + ' .'
        nt.append(temp)

def extract_nurturing(nt):
    """
        Extract nurturing to N-Triples list

        Parameters
        ----------
        nt
            N-Triples dataset
    """
    for key, value in nurturing_list.items():
        # (nurturing_id pred_nurturing nurturing_name)
        temp = base_URI + nurt_id_URI + str(key) + '> '
        temp += base_URI + name_pred_URI + '> '
        temp += value + ' .'
        nt.append(temp)

def extract_animals(nt, dataset):
    """
        Extract animals to N-Triples list

        Parameters
        ----------
        nt
            N-Triples dataset
        dataset
            dataset file loaded list
    """
    for i in range(1, len(dataset)):
        # (animal_id pred_id animal_name)
        temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
        temp += base_URI + name_pred_URI + '> '
        temp += '"' + dataset[i][0].title() + '"' + ' .'
        nt.append(temp)

        # (animal_id pred_class class_id)
        temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
        temp += base_URI + class_pred_URI + '> '
        temp += base_URI + class_id_URI + dataset[i][17] + '> ' + '.'
        nt.append(temp)

        # (animal_id pred_legs legs_num)
        if (dataset[i][13] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + legs_pred_URI + '> '
            temp += '"' + dataset[i][13] + '"' + ' .'
            nt.append(temp)

        # (animal_id pred_nurt nurt_id)
        if (dataset[i][3] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + nurt_pred_URI + '> '
            temp += base_URI + nurt_id_URI + '1> ' + '.'
            nt.append(temp)
        if (dataset[i][4] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + nurt_pred_URI + '> '
            temp += base_URI + nurt_id_URI + '2> ' + '.'
            nt.append(temp)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # (animal_id has tail)
        if (dataset[i][14] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + has_pred_URI + '> '
            temp += '"Tail"' + ' .'
            nt.append(temp)

        # (animal_id has fins)
        if (dataset[i][12] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + has_pred_URI + '> '
            temp += '"Fins"' + ' .'
            nt.append(temp)

        # (animal_id has feathers)
        if (dataset[i][2] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + has_pred_URI + '> '
            temp += '"Feathers"' + ' .'
            nt.append(temp)

        # (animal_id has hair)
        if (dataset[i][1] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + has_pred_URI + '> '
            temp += '"Hair"' + ' .'
            nt.append(temp)
            
        # (animal_id has backbone)
        if (dataset[i][9] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + has_pred_URI + '> '
            temp += '"Backbone"' + ' .'
            nt.append(temp)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # (animal_id is domestic)
        if (dataset[i][15] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Domestic"' + ' .'
            nt.append(temp)

        # (animal_id is venomous)
        if (dataset[i][11] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Venomous"' + ' .'
            nt.append(temp)

        # (animal_id is toothed)
        if (dataset[i][8] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Toothed"' + ' .'
            nt.append(temp)

        # (animal_id is airborne)
        if (dataset[i][5] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Airborne"' + ' .'
            nt.append(temp)

        # (animal_id is aquatic)
        if (dataset[i][6] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Aquatic"' + ' .'
            nt.append(temp)
            
        # (animal_id is predator)
        if (dataset[i][7] != '0'):
            temp = base_URI + animal_id_URI + dataset[i][0].replace(' ','_') + '> '
            temp += base_URI + is_pred_URI + '> '
            temp += '"Predator"' + ' .'
            nt.append(temp)

def save_NT(nt):
    """
        Save a nt dataset file

        Parameters
        ----------
        nt
            N-Triples list to be saved
    """
    f = open('zoo.nt','w')
    for data in nt:
        f.write(str(data) + "\n")
    f.close()

# main entry point
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))