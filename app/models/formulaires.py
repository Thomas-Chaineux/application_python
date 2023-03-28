from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class Recherche(FlaskForm):
    nom_gare = StringField("nom_gare", validators=[]) 
    ligne = SelectMultipleField('ligne', choices=[('', ''), ('CDGVAL', 'CDGVal'), ('FUNICULAIRE', 'FUNICULAIRE MONTMARTRE'), ('M1', 'METRO 1'), ('M2', 'METRO 2'), ('M3', 'METRO 3'), ('M3bis', 'METRO 3bis'), ('M4', 'METRO 4'), ('M5', 'METRO 5'), ('M6', 'METRO 6'), ('M7', 'METRO 7'), ('M7bis', 'METRO 7bis'), ('M8', 'METRO 8'), ('M9', 'METRO 9'), ('M10', 'METRO 10'), ('M11', 'METRO 11'), ('M12', 'METRO 12'), ('M13', 'METRO 13'), ('M14', 'METRO 14'), ('ORLYVAL', 'ORLYVAL'), ('RER A', 'RER A'), ('RER B', 'RER B'), ('RER C', 'RER C'), ('RER D', 'RER D'), ('TRAIN H', 'TRAIN H'), ('TRAIN J', 'TRAIN J'), ('TRAIN K', 'TRAIN K'), ('TRAIN L', 'TRAIN L'), ('TRAIN N', 'TRAIN N'), ('TRAIN P', 'TRAIN P'), ('TRAIN R', 'TRAIN R'), ('TRAIN U', 'TRAIN U'), ('T1', 'TRAM 1'), ('T2', 'TRAM 2'), ('T3', 'TRAM 3'), ('T3a', 'TRAM 3a'), ('T3b', 'TRAM 3b'), ('T4', 'TRAM 4'), ('T5', 'TRAM 5'), ('T6', 'TRAM 6'), ('T7', 'TRAM 7'), ('T8', 'TRAM 8'), ('T9', 'TRAM 9'), ('T10', 'TRAM 10'), ('T11', 'TRAM 11'), ('T12', 'TRAM 12'), ('T13', 'TRAM 13')])

class InsertionGare(FlaskForm):
    code_gare =  StringField("code_gare", validators=[]) 
    nom_gare =  StringField("nom_gare", validators=[])
    introduction =  TextAreaField("code_gare", validators=[]) 
    ligne = SelectMultipleField('ligne', choices=[('', ''), ('CDGVAL', 'CDGVal'), ('FUNICULAIRE', 'FUNICULAIRE MONTMARTRE'), ('M1', 'METRO 1'), ('M2', 'METRO 2'), ('M3', 'METRO 3'), ('M3bis', 'METRO 3bis'), ('M4', 'METRO 4'), ('M5', 'METRO 5'), ('M6', 'METRO 6'), ('M7', 'METRO 7'), ('M7bis', 'METRO 7bis'), ('M8', 'METRO 8'), ('M9', 'METRO 9'), ('M10', 'METRO 10'), ('M11', 'METRO 11'), ('M12', 'METRO 12'), ('M13', 'METRO 13'), ('M14', 'METRO 14'), ('ORLYVAL', 'ORLYVAL'), ('RER A', 'RER A'), ('RER B', 'RER B'), ('RER C', 'RER C'), ('RER D', 'RER D'), ('TRAIN H', 'TRAIN H'), ('TRAIN J', 'TRAIN J'), ('TRAIN K', 'TRAIN K'), ('TRAIN L', 'TRAIN L'), ('TRAIN N', 'TRAIN N'), ('TRAIN P', 'TRAIN P'), ('TRAIN R', 'TRAIN R'), ('TRAIN U', 'TRAIN U'), ('T1', 'TRAM 1'), ('T2', 'TRAM 2'), ('T3', 'TRAM 3'), ('T3a', 'TRAM 3a'), ('T3b', 'TRAM 3b'), ('T4', 'TRAM 4'), ('T5', 'TRAM 5'), ('T6', 'TRAM 6'), ('T7', 'TRAM 7'), ('T8', 'TRAM 8'), ('T9', 'TRAM 9'), ('T10', 'TRAM 10'), ('T11', 'TRAM 11'), ('T12', 'TRAM 12'), ('T13', 'TRAM 13')])

class InsertionLigne(FlaskForm):
    code_ligne =  StringField("code_ligne", validators=[]) 
    nom_ligne =  StringField("nom_ligne", validators=[])

class SuppressionGare(FlaskForm):        
    code_gare =  StringField("code_gare", validators=[]) 
    nom_gare = SelectField("nom_gare", choices=[])

class SuppressionLigne (FlaskForm):        
    code_ligne =  StringField("code_ligne", validators=[]) 
    nom_ligne = SelectField("nom_ligne", choices=[])

class AjoutUtilisateur(FlaskForm):
    prenom = StringField("prenom", validators=[DataRequired(message="Champ prénom obligatoire")])
    mail = StringField("mail", validators=[DataRequired(message="Champ mail obligatoire"),
        Email(message="Le mail saisi n'est pas valide")])
    password = PasswordField("password", validators=[DataRequired(message="Champ mot de passe obligatoire"),
        Length(min=6, message="Le mot de passe fait moins de 6 caractères"),
        EqualTo('password_confirm', message='Les mots de passe doivent être identiques')])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(message="Confirmation de mot de passe obligatoire")])

    def validate_password(self, password):
        if re.search( "[0-9]", password.data) and re.search("[a-z]", password.data) and re.search("[A-Z]", password.data):
            pass
        else:
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre, une minuscule et une majuscule")

class Connexion(FlaskForm):
    mail = StringField("mail", validators=[DataRequired(message="Champ mail obligatoire"),
        Email(message="Le mail saisi n'est pas valide")])
    password = PasswordField("password", validators=[DataRequired(message="Champ mot de passe obligatoire")])