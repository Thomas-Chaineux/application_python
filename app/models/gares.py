from app.app import app, db

gares_lignes = db.Table(
    "gares_lignes",
    db.Column('gareid', db.Integer, db.ForeignKey('gares.codeunique'), primary_key=True),
    db.Column('ligneid', db.Integer, db.ForeignKey('lignes.id'), primary_key=True)
)

gares_modes = db.Table(
    "gares_modes",
    db.Column('gareid', db.Integer, db.ForeignKey('gares.codeunique'), primary_key=True),
    db.Column('modeid', db.Integer, db.ForeignKey('modes.id'), primary_key=True)
)

gares_exploitants = db.Table(
    "gares_exploitants",
    db.Column('gareid', db.Integer, db.ForeignKey('gares.codeunique'), primary_key=True),
    db.Column('exploitantid', db.Integer, db.ForeignKey('exploitants.id'), primary_key=True)
)

class Gares(db.Model):
    __tablename__ = "gares"

    codeunique	= db.Column(db.Integer, primary_key=True)
    nom_long = db.Column(db.String(100))
    label = db.Column(db.String(100))
    id_ref_lda = db.Column(db.Integer)
    nom_lda	= db.Column(db.String(100))
    id_ref_zdl = db.Column(db.Integer)
    nom_zdl = db.Column(db.String(100))
    idrefliga= db.Column(db.String(100))
    idrefligc= db.Column(db.String(100))

    coordonnees = db.relationship('Coordonnees', backref='geom', lazy=True)

    attributs = db.relationship('Attributs', backref='attributss', lazy=True)

    gares_ligness = db.relationship(
        'Lignes', secondary=gares_lignes, backref="gares_ligness")
    
    gares_exploitantss = db.relationship(
        'Exploitants', secondary=gares_exploitants, backref="gares_exploitantss")

    gares_modess = db.relationship('Modes', secondary=gares_modes, backref="gares_modess")




class Coordonnees(db.Model):
    __tablename__ = "coordonnees"
    
    codeunique	= db.Column(db.Integer, db.ForeignKey('gares.codeunique'), primary_key=True)
    geoPoint = db.Column(db.String(200))
    geoShape = db.Column(db.String(200))
    x = db.Column(db.String(50))
    y = db.Column(db.String(50))




class Lignes(db.Model):
    __tablename__="lignes"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))

    lignes = db.relationship(
      'Gares', 
      secondary=gares_lignes, 
      backref="lignes"
    )

class Attributs(db.Model):
    __tablename__ = "attributs"

    valeur = db.Column(db.Integer, primary_key=True)
    relation = db.Column(db.Text)

    id = db.Column(db.Integer, db.ForeignKey('gares.codeunique'))



class Exploitants(db.Model):
    __tablename__ = "exploitants"
    id = db.Column(db.Integer(), primary_key=True)
    label = db.Column(db.Text)




class Modes(db.Model):
    __tablename__ = "modes"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)

   
