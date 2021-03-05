from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Planeta(db.Model):
    __tablename__ = 'Planeta'
    id = db.Column(db.Integer, primary_key=True)
    diametro = db.Column(db.String(250))
    periodo_rotacion = db.Column(db.String(250))
    periodo_orbital = db.Column(db.String(250))
    gravedad = db.Column(db.String(250))
    poblacion = db.Column(db.String(250))
    clima = db.Column(db.String(250))
    terreno= db.Column(db.String(250))
    superfice_acuatica = db.Column(db.String(250))
    creacion= db.Column(db.String(250))
    editado = db.Column(db.String(250))
    nombre = db.Column(db.String(250), nullable=False)    
    
    def serialize(self):
        return {
            "id": self.id,
            "diametro": self.diametro,
            "periodo_rotacion": self.periodo_rotacion,
            "periodo_orbital": self.periodo_orbital,
            "gravedad": self.gravedad,
            "poblacion": self.poblacion,
            "clima": self.clima,
            "terreno": self.terreno,
            "superfice_acuatica": self.superfice_acuatica,
            "creacion": self.creacion,
            "editado": self.editado,
            "nombre": self.nombre
        }


class Personajes(db.Model):
    __tablename__ = 'Personajes'
    id = db.Column(db.Integer, primary_key=True)
    altura= db.Column(db.String(250))
    masa = db.Column(db.String(250))
    color_cabello = db.Column(db.String(250))
    color_piel = db.Column(db.String(250))
    color_ojos= db.Column(db.String(250))
    fecha_nacimiento = db.Column(db.String(250))
    genero = db.Column(db.String(250))
    creacion= db.Column(db.String(250))
    editado = db.Column(db.String(250))
    nombre = db.Column(db.String(250))
    
    def serialize(self):
        return {
            "id": self.id,
            "altura": self.altura,
            "masa": self.masa,
            "color_cabello": self.color_cabello,
            "color_piel": self.color_piel,
            "color_ojos": self.color_ojos,
            "fecha_nacimiento": self.fecha_nacimiento,
            "genero": self.genero,   
            "creacion": self.creacion,
            "editado": self.editado,
            "nombre": self.nombre
            
        }
          

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(250))
    primer_apellido= db.Column(db.String(250))
    segundo_apellido= db.Column(db.String(250))
    email=db.Column(db.String(250))
    password=db.Column(db.String(250))

    def serialize(self):
        return {
              "id": self.id,
              "nombre": self.nombre,
              "primer_apellido": self.primer_apellido,
              "segundo_apellido": self.segundo_apellido,
              "email": self.email,
            
        }

class Favoritos(db.Model):
    __tablename__ = 'Favoritos'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    planeta_id = db.Column(db.Integer,db.ForeignKey('Planeta.id'))
    personajes_id = db.Column(db.Integer,db.ForeignKey('Personajes.id'))
    usuario_id = db.Column(db.Integer,db.ForeignKey('Usuario.id'))
    usuario=db.relationship(Usuario)
    planetas=db.relationship(Planeta)
    personajes=db.relationship(Personajes)

    def serialize(self):
        return {
              "id": self.id,
              "planeta_id": self.planeta_id,
              "personajes_id": self.personajes_id,
              "usuario_id": self.usuario_id
        }

