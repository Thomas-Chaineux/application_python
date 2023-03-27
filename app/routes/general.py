from flask import render_template
from app.app import app, db
from ..models.gares import Gares, Lignes, Attributs
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

#@app.route("/garedetail/<string:codeunique>")
#def garedetail(codeunique):
    query1 = Attributs.query
    dict_detailgare = query1.with_entities(Attributs.relation).filter(Attributs.id == codeunique, Attributs.valeur > 0).all()
    nom_gare = Gares.query.with_entities(Gares.label).filter(Gares.codeunique == codeunique).all()
    return render_template('pages/garedetail.html', donnees=dict_detailgare, gare=nom_gare)

#@app.route("/garedetail/<string:codeunique>")
#def garedetail(codeunique):
    donnees = Attributs.query.with_entities(Attributs.relation).filter(Attributs.id == codeunique, Attributs.valeur > 0)
    
    return render_template('pages/garedetail.html', donnees=donnees, gare=Gares.query.with_entities(Gares.label).filter(Gares.codeunique == codeunique).all())

#@app.route("/garedetail/<string:codeunique>")
#def garedetail(codeunique):
    garedetail=[]

    query= Gares.query

    garedetail = query.filter(Gares.codeunique == codeunique).all()

    return render_template("pages/garedetail.html", codeunique = codeunique, garedetail=garedetail)


#@app.route("/garedetail/<string:codeunique>")
#def garedetail(codeunique):
    garedetail = db.session.query(Attributs).select_from(Gares).join(Gares.attributs).filter(Gares.codeunique == codeunique).all()

    return render_template("pages/garedetail.html", gare = codeunique, donnees=garedetail)


# création de la base de données
conn = db.connect()

#creation d'un curseur qui sera appelé pour la création de la table utiliateur en dehors du csv
c = conn.cursor()

@app.route("/garedetail/<string:codeunique>")
def garedetail(codeunique):
    garedetail = c.execute(f'SELECT relation FROM attributes INNER JOIN gares ON attributs.id = gares.codeunique WHERE attributs.id = {codeunique} and attributs.valeur > 0')

    return render_template("pages/garedetail.html", gare = codeunique, donnees=garedetail)



