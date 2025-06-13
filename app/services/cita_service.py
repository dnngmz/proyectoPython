from app.models.cita import Cita
from app.models.doctor import Doctor
from app.models.mascota import Mascota
from app.services.base_service import BaseService
from app import db

class CitaService(BaseService):
    def __init__(self):
        super().__init__(Cita)

    @staticmethod
    def get_all():
        return Cita.query.all()

    @staticmethod
    def get_by_id(cita_id):
        return Cita.query.get(cita_id)

    @staticmethod
    def create(data):
        required_fields = ['fecha', 'idVeterinario', 'idMascota']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'El campo {field} es requerido')

        if not Doctor.query.get(data['idVeterinario']):
            raise ValueError('Veterinario no válido')
        if not Mascota.query.get(data['idMascota']):
            raise ValueError('Mascota no válida')

        cita = Cita(
            fecha=data['fecha'],
            motivo=data.get('motivo', '').strip(),
            idVeterinario=data['idVeterinario'],
            idMascota=data['idMascota'],
            estado=data.get('estado', True)
        )
        db.session.add(cita)
        db.session.commit()
        return cita

    @staticmethod
    def update(cita_id, data):
        cita = Cita.query.get(cita_id)
        if not cita:
            return None

        for field in ['fecha', 'motivo', 'idVeterinario', 'idMascota', 'estado']:
            if field in data:
                setattr(cita, field, data[field])

        db.session.commit()
        return cita

    @staticmethod
    def delete(cita_id):
        cita = Cita.query.get(cita_id)
        if not cita:
            return False
        db.session.delete(cita)
        db.session.commit()
        return True