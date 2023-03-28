from flask import render_template
from app.app import app, db
from ..models.gares import Gares, Lignes, Attributs, Exploitants, gares_exploitants
import json
from sqlalchemy import or_


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
    
@app.route("/carte")
def carte():
    return render_template('pages/carte.html', donnees=getGeoJSON(Gares.query.all()))

# @app.route("/gares")
# def gares():
#     dictGares = {}
#     for gare in Gares.query.order_by(Gares.label).all():
#         first = gare.label[0]
#         if first in dictGares.keys():
#             dictGares[first].append([gare.codeunique,gare.label])
#         else:
#             dictGares[first]=[[gare.codeunique,gare.label],]
#     return render_template('pages/gares.html', donnees=dictGares)

@app.route("/gares/<int:page>")
def gares(page):
    resultat = Gares.query.order_by(Gares.label).paginate(page=page, per_page=int(app.config["GARES_PER_PAGE"]))
    return render_template('pages/gares.html', pagination=resultat)

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

@app.route("/gare/<string:codeunique>")
def gare(codeunique):
    return render_template('pages/gare.html', id=codeunique, donnees=getGeoJSON([Gares.query.get(codeunique),]))

@app.route("/ligne/<string:id>")
def ligne(id):
    resultat = Lignes.query.get(id)
    return render_template('pages/ligne.html', id=id, resultat = resultat, donnees = getGeoJSON(resultat.lignes))

@app.route("/garedetail/<string:codeunique>")
def garedetail(codeunique):
    
    dict_detailgare = Attributs.query.with_entities(Attributs.relation).filter(Attributs.id == codeunique, Attributs.valeur > 0).all()
    nom_gare = Gares.query.with_entities(Gares.label).filter(Gares.codeunique == codeunique).all()
    referentiel_gare = Gares.query.with_entities(Gares.id_ref_lda, Gares.id_ref_zdl, Gares.idrefliga, Gares.idrefligc).filter(Gares.codeunique == codeunique).all()
    ref_gare = {"référentiel des Lieux d'Arrêt (LDA)": referentiel_gare[0][0],
                "référentiel des Zones de Lieu (ZDL)": referentiel_gare[0][1],
                "référentiel CodifLigne des lignes administratives" : referentiel_gare[0][2],
                "référentiel CodifLigne des lignes commerciales": referentiel_gare[0][3]}
    exploitant = Gares.query.filter(Gares.codeunique == codeunique).all()
    #for exploitantsss in Gares.query.all():
     #   print(exploitantsss.gares_exploitantss.label)
    return render_template('pages/garedetail.html', donnees=dict_detailgare, gare=nom_gare, ref=ref_gare, exploitant=exploitant)




