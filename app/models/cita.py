from datetime import datetime
from app import db

class Cita(db.Model):
    __tablename__ = 'Cita'

    idCita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(255))
    idDoctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    idMascota = db.Column(db.Integer, db.ForeignKey('Mascota.idMascota'))
    estado = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cita {self.idCita} - {self.fecha}>'

    def to_dict(self):
        return {
            'idCita': self.idCita,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'motivo': self.motivo,
            'idDoctor': self.idDoctor,
            'idMascota': self.idMascota,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }