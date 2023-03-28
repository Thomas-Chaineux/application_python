#vérifier que les appels sont les bons
from ..app import app, db
from flask import render_template, request, flash
from ..models.gares import Gare, Ligne
from ..models.formulaires import  Suppression_Gare, Suppression_Ligne
from ..utils.transformations import  clean_arg

@app.route("/suppressions/gare", methods=['GET', 'POST'])
def suppression_gare():
    form = SuppressionGare()
    form.nom_gare.choices = [('','')] + [(gare.id, gare.name) for gare in Gare.query.all()]

    def delete_gare(gare):
        # vérifier que le code existe bien en base
        gare = Gare.query.get(code_gare)
        if gare:
            db.session.delete(gare)
            db.session.commit()

    try:
        if form.validate_on_submit():
            nom_gare =  clean_arg(request.form.get("nom_gare", None))
            code_gare =  clean_arg(request.form.get("code_gare", None))

            if code_gare:
                delete_gare(code_gare)
                flash("La suppression de la gare s'est correctement déroulée", 'info')
            
            elif nom_gare:
                delete_gare(nom_gare)
                flash("La suppression de la gare s'est correctement déroulée", 'info')

            else:
                flash("Il n'y a aucune gare spécifiée", "error")
    
    except Exception as e :
        flash("Une erreur s'est produite lors de la suppression : " + str(e), "error")
    
    return render_template("pages/suppression_gare.html", 
            sous_titre= "Suppression gare" , 
            form=form)

@app.route("/suppressions/ligne", methods=['GET', 'POST'])
def suppression_ligne():
    form = SuppressionLigne()
    form.nom_ligne.choices = [('','')] + [(ligne.id, ligne.name) for ligne in Ligne.query.all()]

    def delete_ligne(ligne):
        # vérifier que le code existe bien en base
        ligne = Resources.query.get(ligne)
        if ligne:
            db.session.delete(ligne)
            db.session.commit()

    try:
        if form.validate_on_submit():
            nom_ligne =  clean_arg(request.form.get("nom_ligne", None))
            code_ligne =  clean_arg(request.form.get("code_ligne", None))

            if code_ligne:
                delete_ligne(code_ligne)
                flash("La suppression de la ligne s'est correctement déroulée", 'info')
            
            elif nom_ligne:
                delete_ligne(nom_ligne)
                flash("La suppression de la ligne s'est correctement déroulée", 'info')

            else:
                flash("Il n'y a aucune ligne spécifiée", "error")
    
    except Exception as e :
        flash("Une erreur s'est produite lors de la suppression : " + str(e), "error")
    
    return render_template("pages/suppression_ligne.html", 
            sous_titre= "Suppression ligne" , 
            form=form)
