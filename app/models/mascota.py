from datetime import datetime
from app import db

class Mascota(db.Model):
    __tablename__ = 'Mascota'

    idMascota = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50))
    raza = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    URL = db.Column(db.String(255))
    idCliente = db.Column(db.Integer, db.ForeignKey('Cliente.idCliente'), nullable=False)

    # Relaciones
    citas = db.relationship('Cita', backref='mascota', lazy=True, cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Mascota {self.nombre}>'

    def to_dict(self):
        return {
            'idMascota': self.idMascota,
            'nombre': self.nombre,
            'especie': self.especie,
            'raza': self.raza,
            'edad': self.edad,
            'URL': self.URL,
            'idCliente': self.idCliente,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }