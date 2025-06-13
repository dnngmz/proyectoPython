from datetime import datetime
from app import db

class Cliente(db.Model):
    __tablename__ = 'Cliente'

    idCliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)

    # Relaciones
    mascotas = db.relationship('Mascota', backref='cliente', lazy=True, cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

    def to_dict(self):
        return {
            'idCliente': self.idCliente,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None#,
            #'mascotas': [mascota.to_dict() for mascota in self.mascotas]
        }