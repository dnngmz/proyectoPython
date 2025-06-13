from flask import Blueprint, request
from app.services.cita_service import CitaService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required

cita_bp = Blueprint('citas', __name__)
cita_service = CitaService()

class CitaController(BaseController):
    def __init__(self):
        super().__init__(cita_service)

    @staticmethod
    @cita_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        try:
            citas = CitaService.get_all()
            return CitaController.success_response(
                data=[c.to_dict() for c in citas],
                message=f'Se encontraron {len(citas)} citas'
            )
        except Exception as e:
            return CitaController.error_response(f'Error al obtener citas: {str(e)}', 500)

    @staticmethod
    @cita_bp.route('/<int:id>', methods=['GET'])
    @token_required
    def get_by_id(id):
        try:
            cita = CitaService.get_by_id(id)
            if not cita:
                return CitaController.error_response('Cita no encontrada', 404)
            return CitaController.success_response(cita.to_dict())
        except Exception as e:
            return CitaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @cita_bp.route('', methods=['POST'])
    def create():
        try:
            data = request.get_json()
            cita = CitaService.create(data)
            return CitaController.success_response(cita.to_dict(), "Cita creada", 201)
        except Exception as e:
            return CitaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @cita_bp.route('/<int:id>', methods=['PUT'])
    @token_required
    def update(id):
        try:
            data = request.get_json()
            cita = CitaService.update(id, data)
            if not cita:
                return CitaController.error_response("Cita no encontrada", 404)
            return CitaController.success_response(cita.to_dict(), "Actualizada correctamente")
        except Exception as e:
            return CitaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @cita_bp.route('/<int:id>', methods=['DELETE'])
    @token_required
    def delete(id):
        try:
            success = CitaService.delete(id)
            if not success:
                return CitaController.error_response("Cita no encontrada", 404)
            return CitaController.success_response(message="Cita eliminada")
        except Exception as e:
            return CitaController.error_response(f'Error: {str(e)}', 500)

cita_controller = CitaController()