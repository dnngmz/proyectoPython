from app.models.mascota import Mascota
from app.models.cliente import Cliente
from app.services.base_service import BaseService
from app import db

class MascotaService(BaseService):
    def __init__(self):
        super().__init__(Mascota)

    @staticmethod
    def get_all():
        return Mascota.query.all()

    @staticmethod
    def get_by_id(mascota_id):
        return Mascota.query.get(mascota_id)

    @staticmethod
    def create(data):
        required_fields = ['nombre', 'idCliente']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'El campo {field} es requerido')

        cliente = Cliente.query.get(data['idCliente'])
        if not cliente:
            raise ValueError('Cliente no válido')

        mascota = Mascota(
            nombre=data.get('nombre').strip(),
            especie=data.get('especie', '').strip(),
            raza=data.get('raza', '').strip(),
            edad=data.get('edad'),
            URL=data.get('URL', '').strip(),
            idCliente=data.get('idCliente')
        )
        db.session.add(mascota)
        db.session.commit()
        return mascota

    @staticmethod
    def update(mascota_id, data):
        mascota = Mascota.query.get(mascota_id)
        if not mascota:
            return None

        for field in ['nombre', 'especie', 'raza', 'edad', 'URL', 'idCliente']:
            if field in data:
                setattr(mascota, field, data[field])

        db.session.commit()
        return mascota

    @staticmethod
    def delete(mascota_id):
        mascota = Mascota.query.get(mascota_id)
        if not mascota:
            return False
        db.session.delete(mascota)
        db.session.commit()
        return True