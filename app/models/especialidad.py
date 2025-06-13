from datetime import datetime
from app import db

class Especialidad(db.Model):
    __tablename__ = 'Especialidad'

    idEspecialidad = db.Column(db.Integer, primary_key=True)
    nombreEspecialidad = db.Column(db.String(100), nullable=False)

    # Relaciones
    doctores = db.relationship('Doctor', backref='especialidad', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Especialidad {self.nombreEspecialidad}>'

    def to_dict(self):
        return {
            'idEspecialidad': self.idEspecialidad,
            'nombreEspecialidad': self.nombreEspecialidad,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }