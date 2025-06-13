from app.models.doctor import Doctor
from app.models.especialidad import Especialidad
from app.services.base_service import BaseService
from app import db

class DoctorService(BaseService):
    def __init__(self):
        super().__init__(Doctor)

    @staticmethod
    def get_all():
        return Doctor.query.all()

    @staticmethod
    def get_by_id(doctor_id):
        return Doctor.query.get(doctor_id)

    @staticmethod
    def create(data):
        nombre = data.get('nombre', '').strip()
        telefono = data.get('telefono', '').strip()
        email = data.get('email', '').strip().lower()
        idEspecialidad = data.get('idEspecialidad')

        if not nombre or not idEspecialidad:
            raise ValueError('Nombre y especialidad son requeridos')

        especialidad = Especialidad.query.get(idEspecialidad)
        if not especialidad:
            raise ValueError('Especialidad no válida')

        doctor = Doctor(nombre=nombre, telefono=telefono, email=email, idEspecialidad=idEspecialidad)
        db.session.add(doctor)
        db.session.commit()
        return doctor

    @staticmethod
    def update(doctor_id, data):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None

        for field in ['nombre', 'telefono', 'email', 'idEspecialidad']:
            if field in data:
                setattr(doctor, field, data[field].strip() if isinstance(data[field], str) else data[field])

        db.session.commit()
        return doctor

    @staticmethod
    def delete(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return False
        db.session.delete(doctor)
        db.session.commit()
        return True