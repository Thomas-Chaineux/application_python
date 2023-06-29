from flask import render_template
from app.app import app
from ..models.gares import Gares, Lignes, Attributs
import json


@app.route("/")
@app.route("/home")
def home():
    return render_template('pages/index.html')

def getGeoJSON(query) :
    geoJSONfeatures= []
    for gare in query:
        lignes = [[ligne.id,ligne.label] for ligne in gare.lignes]
        geojsonFeature = {
            "type": "Feature",
            "properties": {
                "id":gare.codeunique,
                "name": gare.nom_long,
                "label":gare.label,
                "geoPoint":gare.coordonnees[0].geoPoint.split(', '),
                "lignes": lignes
            },
            "geometry": json.loads(gare.coordonnees[0].geoShape)
        }
        geoJSONfeatures.append(geojsonFeature)
    return {"type" : "FeatureCollection", "features":geoJSONfeatures}

#route pour la carte générale des gares    
@app.route("/carte")
def carte():
    return render_template('pages/carte.html', donnees=getGeoJSON(Gares.query.all()))

#route pour la liste des gares par ordre alphabétique des noms de gare, avec une pagination définie comme dans le fichier .env
@app.route("/gares/<int:page>")
def gares(page):
    resultat = Gares.query.order_by(Gares.label).paginate(page=page, per_page=int(app.config["GARES_PER_PAGE"]))
    return render_template('pages/gares.html', pagination=resultat)

#route pour une page reprenant les différentes lignes (métro, train, RER, ...)
@app.route("/lignes")
def lignes():
    dictLignes = {}
    for ligne in Lignes.query.order_by(Lignes.label).all():
        first = ligne.label[0]
        if first in dictLignes.keys():
            dictLignes[first].append([ligne.id,ligne.label])
        else:
            dictLignes[first]=[[ligne.id,ligne.label],]
    return render_template('pages/lignes.html', donnees=dictLignes)

#route pour afficher chaque gare séparément sur la carte
@app.route("/gare/<string:codeunique>")
def gare(codeunique):
    return render_template('pages/gare.html', id=codeunique, donnees=getGeoJSON([Gares.query.get(codeunique)]))

#route pour afficher toutes les gares qui sont situées sur une même ligne
@app.route("/ligne/<string:id>")
def ligne(id):
    resultat = Lignes.query.get(id)
    return render_template('pages/ligne.html', id=id, resultat = resultat, donnees = getGeoJSON(resultat.lignes))

#route pour les données sur le réseau et les identifiants de la gare
@app.route("/garedetail/<string:codeunique>")
def garedetail(codeunique):  
    detailgare = Attributs.query.with_entities(Attributs.relation).filter(Attributs.id == codeunique, Attributs.valeur > 0).all()    
    gare_cible = Gares.query.filter(Gares.codeunique == codeunique).all()
    return render_template('pages/garedetail.html', donnees=detailgare, gare_cible=gare_cible)