import pandas as pd
import sqlite3 as db
import numpy as np
import os
import sys
from datetime import datetime
import re


# variables 
GARES_CSV_FILEPATH = "./emplacement-des-gares-idf-data-generalisee.csv"
GARES_SQLITE_FILEPATH = "./gares.sqlite"
DATATYPES = {'id_ref_lda': np.int64,
           'id_ref_zdl': np.int64,
           'idrefliga': 'str',
           'idrefligc': 'str',
           'codeunique': np.int64,
           'x': 'str',
           'y': 'str',
           'fer':'bool',
           'train':'bool',
           'rer':'bool',
           'metro':'bool',
           'tramway':'bool',
           'navette':'bool',
           'val':'bool',
           'terfer':'bool',
           'tertrain':'bool',
           'terrer':'bool',
           'termetro':'bool',
           'tertram':'bool',
           'ternavette':'bool',
           'terval':'bool',
           'principal':'bool',
           'idf':'bool'}

# quelques fonctions utiles 
def split_multivalue(valeur):
    return (re.sub(r'([A-z0-9])/([A-z0-9])', r'\1 / \2', valeur)).split(" / ")

def create_df_attribut(df_entree, nom_colonne_valeur, nom_relation):
    df = df_entree[["codeunique", nom_colonne_valeur]]
    df = df.rename(columns={nom_colonne_valeur: 'valeur', 'codeunique':'id'})
    df["relation"] = nom_relation
    return df


#############################

try:
    # suppression de la base existante
    os.remove(GARES_SQLITE_FILEPATH)
except:
    pass

# création de la base de données
conn = db.connect(GARES_SQLITE_FILEPATH)

#creation d'un curseur qui sera appelé pour la création de la table utiliateur en dehors du csv
c = conn.cursor()

# création du dataframe pandas à partir du csv
df= pd.read_csv(filepath_or_buffer=GARES_CSV_FILEPATH,
    sep=";",
    header=0)


# modif types
df = df.astype(DATATYPES)

##########
#remplissage table des lignes
##########
print(str(datetime.now()) + " Création des données pour la table lignes")
lignes = df.loc[:, 'res_com'].unique()

lignes_distinctes = []

for ligne in lignes:
    # séparer les valeurs multivaluées
    lignes_distinctes = lignes_distinctes  + split_multivalue(ligne)

lignes_distinctes_dedoublonnees = []
for l in lignes_distinctes:
    if l not in lignes_distinctes_dedoublonnees:
        lignes_distinctes_dedoublonnees.append(l)

df_lignes = pd.DataFrame({"label":lignes_distinctes_dedoublonnees})

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    df_lignes.to_sql(
        name='lignes', 
        con=conn,
        index=True,
        index_label="id",
        method="multi"
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()


##########
#remplissage table des modes
##########
print(str(datetime.now()) + " Création des données pour la table modes")
modes = df.loc[:, 'mode'].unique()

modes_distincts = []

for mode in modes:
    modes_distincts = modes_distincts  +split_multivalue(mode)

modes_distincts_dedoublonnes = []
for m in modes_distincts:
    if m not in modes_distincts_dedoublonnes:
        modes_distincts_dedoublonnes.append(m)

df_modes = pd.DataFrame({"label":modes_distincts_dedoublonnes})

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    df_modes.to_sql(
        name='modes', 
        con=conn,
        index=True,
        index_label="id",
        method="multi"
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()


##########
#remplissage table des exploitants
##########
print(str(datetime.now()) + " Création des données pour la table exploitants")
exploitants = df.loc[:, 'exploitant'].unique()

exploitants_distincts = []

for exploitant in exploitants:
    exploitants_distincts = exploitants_distincts  + split_multivalue(exploitant)

exploitants_distincts_dedoublonnes = []
for e in exploitants_distincts:
    if e not in exploitants_distincts_dedoublonnes:
        exploitants_distincts_dedoublonnes.append(e)

df_exploitants = pd.DataFrame({"label":exploitants_distincts_dedoublonnes})

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    df_exploitants.to_sql(
        name='exploitants', 
        con=conn,
        index=True,
        index_label="id",
        method="multi"
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

##########
#remplissage table des gares (hors coordonnées géographiques et attributs booléens)
##########
print(str(datetime.now()) + " Création des données pour la table gares")
gares = df[["codeunique", "nom_long", "label", "id_ref_lda", "nom_lda", "id_ref_zdl", "nom_zdl", "idrefliga","idrefligc"]]

gares = gares.astype({"id_ref_lda": DATATYPES["id_ref_lda"],
              "id_ref_zdl": DATATYPES["id_ref_zdl"],
              "idrefliga": DATATYPES["idrefliga"],
              "idrefligc": DATATYPES["idrefligc"]})

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    gares.to_sql(
        name='gares', 
        con=conn,
        index=False,
        method="multi"
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

##########
#remplissage table des coordonnées des gares
##########
print(str(datetime.now()) + " Création des données pour la table coordonnees")
coordonnees = df[["codeunique", "Geo Point", "Geo Shape", "x", "y"]]
coordonnees.rename(columns={"Geo Point":"geoPoint", "Geo Shape":"geoShape"}, inplace=True)

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    coordonnees.to_sql(
        name='coordonnees', 
        con=conn,
        index=False,
        method="multi"
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()


##########
#remplissage table des flags des attributs flagés
##########
print(str(datetime.now()) + " Création des données pour la table attributs")

table_attributs = pd.concat([create_df_attribut(df, 'fer',"est desservie par une ligne ferrée (TRAIN ou RER)"),
                             create_df_attribut(df, 'train',"est desservie par une ligne ferrée (TRAIN)"),
                             create_df_attribut(df, 'rer',"est desservie par une ligne ferrée (RER)"),
                             create_df_attribut(df, 'metro',"est desservie par une ligne de métro"),
                             create_df_attribut(df, 'tramway',"est desservie par une ligne de tramway"),
                             create_df_attribut(df, 'navette',"est desservie par une ligne dite navette (funiculaire ou val)"),
                             create_df_attribut(df, 'val',"est desservie par une ligne dite val"),
                             create_df_attribut(df, 'terfer',"est terminus d'une ligne ferrée (TRAIN ou RER)"),
                             create_df_attribut(df, 'tertrain',"est terminus d'une ligne ferrée (TRAIN)"),
                             create_df_attribut(df, 'terrer',"est terminus d'une ligne ferrée (RER)"),
                             create_df_attribut(df, 'termetro',"est terminus d'une ligne de métro"),
                             create_df_attribut(df, 'tertram',"est terminus d'une ligne de tramway"),
                             create_df_attribut(df, 'ternavette',"est terminus d'une ligne dite navette (funicualire ou val)"),
                             create_df_attribut(df, 'terval',"est terminus d'une ligne dite val"),
                             create_df_attribut(df, 'principal',"est une gare considérée comme principale"),
                             create_df_attribut(df, 'idf',"est en Île de France")])


# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    table_attributs.to_sql(
        name='attributs', 
        con=conn,
        index=False
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

# faire relations entre gares et lignes, modes et exploitants

##########
#remplissage table des flags gares_lignes
##########
print(str(datetime.now()) + " Création des données pour la table gares_lignes")

gl = df[["codeunique", "res_com"]]

donnees = []

for index, row in gl.iterrows():
    valeurs = split_multivalue(row["res_com"])
    # pour chaque valeur, sélection de l'objet correspondant en base
    for v in valeurs:
        o = conn.cursor().execute("select id from lignes where label = '" +v+ "'").fetchone()[0]
        donnees.append([row["codeunique"], o])
        
gl = pd.DataFrame(donnees,  columns=['gareid', 'ligneid'])

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    gl.to_sql(
        name='gares_lignes', 
        con=conn,
        index=False
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

##########
#remplissage table des flags gares_modes
##########
print(str(datetime.now()) + " Création des données pour la table gares_modes")

gm = df[["codeunique", "mode"]]

donnees = []

for index, row in gm.iterrows():
    valeurs = split_multivalue(row["mode"])
    # pour chaque valeur, sélection de l'objet correspondant en base
    for v in valeurs:
        o = conn.cursor().execute("select id from modes where label = '" +v+ "'").fetchone()[0]
        donnees.append([row["codeunique"], o])

gm = pd.DataFrame(donnees,  columns=['gareid', 'modeid'])

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    gm.to_sql(
        name='gares_modes', 
        con=conn,
        index=False
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

##########
#remplissage table des flags gares_exploitants
##########
print(str(datetime.now()) + " Création des données pour la table gares_exploitants")

ge = df[["codeunique", "exploitant"]]

donnees = []

for index, row in ge.iterrows():
    valeurs = split_multivalue(row["exploitant"])
    # pour chaque valeur, sélection de l'objet correspondant en base
    for v in valeurs:
        o = conn.cursor().execute("select id from exploitants where label = '" +v+ "'").fetchone()[0]
        donnees.append([row["codeunique"], o])

ge = pd.DataFrame(donnees,  columns=['gareid', 'exploitantid'])

# création table et insertion des données
try:
    print(str(datetime.now()) +  " Début de l'insertion des données")
    ge.to_sql(
        name='gares_exploitants', 
        con=conn,
        index=False
        )
    print(str(datetime.now()) + " Données correctement insérées")
except Exception as e :
    print(e)
    sys.exit()

##########
#Création d'une table d'utilisateurs, en dehors du fichier .csv
##########
try:
    print(str(datetime.now()) + " Création d'une table utilisateurs")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, prenom NVARCHAR(20), mail NVARCHAR (50), password NVARCHAR(20), administrateur INTEGER DEFAULT 0, mdp_crypte INTEGER DEFAULT 1)")
    print(str(datetime.now()) + " Table correctement créée")

except Exception as e:
    print(e)
    sys.exit()


##########
#Définition d'un profil d'administrateur à l'initialisation de la base (données à entrer sur le terminal Linux)
##########

username = input("Entrez un nom d'utilisateur : ")
mail = input("Entrez une adresse e-mail : ")
password = input("Entrez un mot de passe temporaire: ")

try:
    df = pd.DataFrame({'prenom': [username], 'password': [password], 'mail' : [mail], 'administrateur': 1, 'mdp_crypte' : 0 })
    df.to_sql('users', conn, if_exists='append', index=False)
    print(str(datetime.now()) + " Profil Administrateur correctement crée")
    print('LE MOT DE PASSE EST TEMPORAIRE ET SERA CHANGE A LA PREMIERE CONNEXION')

except Exception as e:
    print(e)
    sys.exit

conn.close()

