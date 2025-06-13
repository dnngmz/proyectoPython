from flask import Blueprint, request
from app.services.cliente_service import ClienteService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required

cliente_bp = Blueprint('clientes', __name__)
cliente_service = ClienteService()

class ClienteController(BaseController):
    """Controlador para operaciones de Cliente"""

    def __init__(self):
        super().__init__(cliente_service)

    @staticmethod
    @cliente_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        """Obtener todos los clientes (requiere token válido)"""
        try:
            clientes = ClienteService.get_all()
            return ClienteController.success_response(
                data=[cliente.to_dict() for cliente in clientes],
                message=f'Se encontraron {len(clientes)} clientes'
            )
        except Exception as e:
            return ClienteController.error_response(f'Error al obtener clientes: {str(e)}', 500)

    @staticmethod
    @cliente_bp.route('/<int:cliente_id>', methods=['GET'])
    @token_required
    def get_by_id(cliente_id):
        """Obtener cliente por ID"""
        try:
            cliente = ClienteService.get_by_id(cliente_id)
            if not cliente:
                return ClienteController.error_response('Cliente no encontrado', 404)

            return ClienteController.success_response(
                data=cliente.to_dict(),
                message='Cliente encontrado'
            )
        except Exception as e:
            return ClienteController.error_response(f'Error al obtener cliente: {str(e)}', 500)

    @staticmethod
    @cliente_bp.route('', methods=['POST'])
    def create():
        """Registrar nuevo cliente (no requiere token)"""
        try:
            data = request.get_json()
            if not data:
                return ClienteController.error_response('Datos JSON requeridos', 400)

            required_fields = ['nombre', 'email', 'password']
            missing_fields = [f for f in required_fields if not data.get(f)]
            if missing_fields:
                return ClienteController.error_response(
                    f'Campos requeridos: {", ".join(missing_fields)}', 400
                )

            cliente = ClienteService.create(data)
            return ClienteController.success_response(
                data=cliente.to_dict(),
                message=f'Cliente {cliente.nombre} registrado exitosamente',
                status_code=201
            )
        except ValueError as e:
            return ClienteController.error_response(str(e), 400)
        except Exception as e:
            return ClienteController.error_response(f'Error al registrar cliente: {str(e)}', 500)

    @staticmethod
    @cliente_bp.route('/<int:cliente_id>', methods=['PUT'])
    @token_required
    def update(cliente_id):
        """Actualizar datos de un cliente"""
        try:
            data = request.get_json()
            if not data:
                return ClienteController.error_response('Datos JSON requeridos', 400)

            cliente = ClienteService.update(cliente_id, data)
            if not cliente:
                return ClienteController.error_response('Cliente no encontrado', 404)

            return ClienteController.success_response(
                data=cliente.to_dict(),
                message=f'Cliente {cliente.nombre} actualizado exitosamente'
            )
        except ValueError as e:
            return ClienteController.error_response(str(e), 400)
        except Exception as e:
            return ClienteController.error_response(f'Error al actualizar cliente: {str(e)}', 500)

    @staticmethod
    @cliente_bp.route('/<int:cliente_id>', methods=['DELETE'])
    @token_required
    def delete(cliente_id):
        """Eliminar cliente por ID"""
        try:
            success = ClienteService.delete(cliente_id)
            if not success:
                return ClienteController.error_response('Cliente no encontrado', 404)

            return ClienteController.success_response(
                message='Cliente eliminado exitosamente'
            )
        except Exception as e:
            return ClienteController.error_response(f'Error al eliminar cliente: {str(e)}', 500)

cliente_controller = ClienteController()