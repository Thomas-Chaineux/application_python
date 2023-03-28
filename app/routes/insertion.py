#vérifier que les appels sont les bons
from ..app import app, db
from flask import render_template, request, flash
from ..models.gare import Gare, Ligne
from ..models.formulaires import insertion_gare, insertion_ligne
from ..utils.transformations import  clean_arg

@app.route("/insertions/gare", methods=['GET', 'POST'])
def insertion_gare():
    form = InsertionGare() 

    try:
        if form.validate_on_submit():
            nom_gare =  clean_arg(request.form.get("nom_gare", None))
            code_gare =  clean_arg(request.form.get("code_gare", None))
            introduction =  clean_arg(request.form.get("introduction", None))
            lignes =  clean_arg(request.form.getlist("ligne", None))

            nouvelle_gare = Gare(id=code_gare, 
                Introduction=introduction,
                name=nom_gare)

            for ligne in lignes:
                ligne = Lignes.\
                    query.\
                    filter(Lignes.id == ligne).\
                    first()
                nouvelle_gare.resources.append(ligne)
#Rajouter la nouvelle gare sur la carte, rajouter input des coordonnées géographiques en amont            
#            nouvelle_gare.maps.append(Map.query.filter(Map.name==continent).first())

            db.session.add(nouvelle_gare)
            db.session.commit()

            flash("L'insertion de la gare "+ nom_gare + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        flash("Une erreur s'est produite lors de l'insertion de " + nom_gare + " : " + str(e), "error")

        db.session.rollback()
    
    return render_template("pages/insertion_gare.html", 
            sous_titre= "Insertion gare" , 
            form=form)

@app.route("/insertions/ligne", methods=['GET', 'POST'])
def insertion_ligne():
    form = InsertionLigne() 
# Manquant : ajout des gares traversées par la ligne
    try:
        if form.validate_on_submit():
            nom_ligne =  clean_arg(request.form.get("nom_ligne", None))
            id_ligne =  clean_arg(request.form.get("code_ligne", None))

            nouvelle_ressource = Lignes(id=id_ligne, 
                name=nom_ligne)

            db.session.add(nouvelle_ligne)
            db.session.commit()

            flash("L'insertion de la ligne "+ nom_ligne + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        flash("Une erreur s'est produite lors de l'insertion de " + nom_ligne + " : " + str(e), "error")

        db.session.rollback()
    
    return render_template("pages/insertion_ligne.html", 
            sous_titre= "Insertion ressource" , 
            form=form)