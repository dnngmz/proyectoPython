from app.models.cliente import Cliente
from app.services.base_service import BaseService
from app import db

class ClienteService(BaseService):
    """Servicio para operaciones específicas de Cliente"""

    def __init__(self):
        super().__init__(Cliente)

    @staticmethod
    def get_all():
        """Obtener todos los clientes"""
        return Cliente.query.all()

    @staticmethod
    def get_by_id(cliente_id):
        """Obtener cliente por ID"""
        return Cliente.query.get(cliente_id)

    @staticmethod
    def get_by_email(email):
        """Obtener cliente por email"""
        return Cliente.query.filter_by(email=email.lower().strip()).first()

    @staticmethod
    def delete(cliente_id):
        """Eliminar cliente por ID"""
        try:
            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                return False

            db.session.delete(cliente)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def create(data):
        """Crear nuevo cliente con validaciones"""
        required_fields = ['nombre', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f'El campo {field} es requerido')

        nombre = data.get('nombre').strip()
        email = data.get('email').strip().lower()
        password = data.get('password').strip()
        telefono = data.get('telefono', '').strip() if data.get('telefono') else None

        if len(nombre) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')

        if '@' not in email:
            raise ValueError('Email inválido')

        if len(password) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')

        if telefono and len(telefono) < 7:
            raise ValueError('El teléfono debe tener al menos 7 caracteres')

        if Cliente.query.filter_by(email=email).first():
            raise ValueError('El email ya está registrado')

        cliente = Cliente(
            nombre=nombre,
            email=email,
            password=password,
            telefono=telefono
        )

        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def update(cliente_id, data):
        """Actualizar los datos de un cliente existente"""
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return None

        if 'nombre' in data:
            nombre = data['nombre'].strip()
            if len(nombre) < 3:
                raise ValueError('El nombre debe tener al menos 3 caracteres')
            cliente.nombre = nombre

        if 'email' in data:
            email = data['email'].strip().lower()
            if '@' not in email:
                raise ValueError('Email inválido')
            existing = Cliente.query.filter(Cliente.email == email, Cliente.idCliente != cliente_id).first()
            if existing:
                raise ValueError('El email ya está registrado por otro cliente')
            cliente.email = email

        if 'telefono' in data:
            telefono = data['telefono'].strip()
            if telefono and len(telefono) < 7:
                raise ValueError('El teléfono debe tener al menos 7 caracteres')
            cliente.telefono = telefono

        if 'password' in data:
            password = data['password'].strip()
            if len(password) < 6:
                raise ValueError('La contraseña debe tener al menos 6 caracteres')
            cliente.password = password

        db.session.commit()
        return cliente