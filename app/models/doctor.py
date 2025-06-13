from datetime import datetime
from app import db

class Doctor(db.Model):
    __tablename__ = 'Doctor'

    idDoctor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    idEspecialidad = db.Column(db.Integer, db.ForeignKey('Especialidad.idEspecialidad'))

    # Relaciones
    citas = db.relationship('Cita', backref='doctor', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Doctor {self.nombre}>'

    def to_dict(self):
        return {
            'idDoctor': self.idDoctor,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'idEspecialidad': self.idEspecialidad,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }