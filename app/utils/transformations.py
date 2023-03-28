import re

def nettoyage_string_to_int(chaine):
    # Dans le cas où plusieurs informations sont données dans la chaine comme 
    # <strong>Saint Helena: </strong>60 km<br> <strong>Ascension Island: </strong>NA<br> <strong>Tristan da Cunha (island only): </strong>34 km
    # il faut retourner la somme de ces nombligne
    ligne = None

    def clean(ch):
        ligne = re.sub(r'\(.*\)', '', ch) # pour supprimer les dates entre parenthèses
        ligne = re.sub(r'[^0-9\.]*', '', ligne) # pour supprimer tous les carctères sauf les points
        ligne = re.sub(r'\..*', '', ligne) # pour supprimer toutes les décimales
        if ligne:
            ligne = int(ligne)
        else:
            ligne = None
        return ligne
    
    if chaine :
        # cas normal 
        if "<" not in chaine:
            ligne = clean(chaine)
        # cas de la somme
        else :
            tmp = 0
            for el in chaine.split("<br"):
                tmp = tmp + int(clean(el))
            ligne = tmp
    return ligne

def clean_arg(arg):
    if arg == "":
        return None
    else:
        return arg