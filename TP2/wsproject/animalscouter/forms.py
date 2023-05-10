from django import forms
from django.forms import widgets

class_list = [
    (-1, 'Select Animal Class'),
    (1, 'Mammal'),
    (2, 'Bird'),
    (3, 'Reptile'),
    (4, 'Fish'),
    (5, 'Amphibian'),
    (6, 'Insect'),
    (7, 'Invertebrate'),
    ]

nurturing_list = [
    (-1, 'Select Animal Nurturing'),
    (1, 'Eggs'),
    (2, 'Milk'),
    (3, 'Both'),
    ]

legs_list = [
    (-1, 'Select Animal Legs'),
    (0, '0'),
    (2, '2'),
    (4, '4'),
    (6, '6'),
    (8, '8'),
    ]

class CustomSelect(forms.Select):
    def __init__(self, attrs=None, choices=()):
        self.custom_attrs = {-1: {'hidden': 'hidden', 'selected': 'selected'}}
        super().__init__(attrs, choices)

    def create_option(self, name: str, value, label, selected, index, subindex=None, attrs=None):
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        # setting the attributes here for the option
        if len(self.custom_attrs) > 0:
            if value in self.custom_attrs:
                custom_attr = self.custom_attrs[value]
                for k, v in custom_attr.items():
                    option_attrs.update({k: v})

        #self.attrs = {"onChange": "form.submit();"}

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }

"""
    configs.html forms
"""

class InsertAnimalForm(forms.Form):
    animal_class = forms.ChoiceField(choices=class_list, widget=CustomSelect)

    animal_domestic = forms.BooleanField(required=False)
    animal_toothed = forms.BooleanField(required=False)
    animal_venomous = forms.BooleanField(required=False)
    animal_aquatic = forms.BooleanField(required=False)
    animal_airborne = forms.BooleanField(required=False)
    animal_predator = forms.BooleanField(required=False)

    animal_tail = forms.BooleanField(required=False)
    animal_fins = forms.BooleanField(required=False)
    animal_feathers = forms.BooleanField(required=False)
    animal_hair = forms.BooleanField(required=False)
    animal_backbone = forms.BooleanField(required=False)

    animal_milk = forms.BooleanField(required=False)
    animal_eggs = forms.BooleanField(required=False)

    animal_legs = forms.ChoiceField(choices=legs_list, widget=CustomSelect)

    insert_animal_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Animal Name'}))


class DeleteAnimalForm(forms.Form):
    delete_animal_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Animal Name'}))

"""
    queries.html forms
"""

class AnimalClassForm(forms.Form):
    animal_class = forms.ChoiceField(choices=class_list, 
                                   widget=CustomSelect)
    
    # submit form on select item change
    animal_class.widget.attrs.update(onChange="form.submit();")


class AnimalNurturingForm(forms.Form):
    animal_nurturing = forms.ChoiceField(choices=nurturing_list, 
                                   widget=CustomSelect)
    
    # submit form on select item change
    animal_nurturing.widget.attrs.update(onChange="form.submit();")


class AnimalLegsForm(forms.Form):
    animal_legs = forms.ChoiceField(choices=legs_list, 
                                   widget=CustomSelect)
    
    # submit form on select item change
    animal_legs.widget.attrs.update(onChange="form.submit();")

"""
    ask.html forms
"""

question_list = [
    (-1, 'Select Question'),
    ('has_tail', 'Has tail'),
    ('has_fins', 'Has fins'),
    ('has_feathers', 'Has feathers'),
    ('has_hair', 'Has hair'),
    ('has_backbone', 'Has backbone'),
    ('is_domestic', 'Is domestic'),
    ('is_venomous', 'Is venomous'),
    ('is_toothed', 'Is toothed'),
    ('is_airborne', 'Is airborne'),
    ('is_aquatic', 'Is aquatic'),
    ('is_predator', 'Is predator'),
    ]

class AnimalAskForm(forms.Form):
    animal_question = forms.ChoiceField(choices=question_list, 
                                   widget=CustomSelect)
    
    # submit form on select item change
    animal_question.widget.attrs.update(onChange="form.submit();")

    animal_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Animal Name'}))