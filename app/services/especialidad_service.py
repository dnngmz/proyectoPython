from app.models.especialidad import Especialidad
from app.services.base_service import BaseService
from app import db

class EspecialidadService(BaseService):
    def __init__(self):
        super().__init__(Especialidad)

    @staticmethod
    def get_all():
        return Especialidad.query.all()

    @staticmethod
    def get_by_id(especialidad_id):
        return Especialidad.query.get(especialidad_id)

    @staticmethod
    def create(data):
        nombre = data.get('nombreEspecialidad', '').strip()
        if not nombre:
            raise ValueError('El nombre de la especialidad es requerido')

        especialidad = Especialidad(nombreEspecialidad=nombre)
        db.session.add(especialidad)
        db.session.commit()
        return especialidad

    @staticmethod
    def update(especialidad_id, data):
        especialidad = Especialidad.query.get(especialidad_id)
        if not especialidad:
            return None

        if 'nombreEspecialidad' in data:
            especialidad.nombreEspecialidad = data['nombreEspecialidad'].strip()

        db.session.commit()
        return especialidad

    @staticmethod
    def delete(especialidad_id):
        especialidad = Especialidad.query.get(especialidad_id)
        if not especialidad:
            return False
        db.session.delete(especialidad)
        db.session.commit()
        return True