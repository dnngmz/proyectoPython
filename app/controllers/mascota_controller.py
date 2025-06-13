from flask import Blueprint, request
from app.services.mascota_service import MascotaService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required

mascota_bp = Blueprint('mascotas', __name__)
mascota_service = MascotaService()

class MascotaController(BaseController):
    def __init__(self):
        super().__init__(mascota_service)

    @staticmethod
    @mascota_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        try:
            mascotas = MascotaService.get_all()
            return MascotaController.success_response(
                data=[m.to_dict() for m in mascotas],
                message=f'Se encontraron {len(mascotas)} mascotas'
            )
        except Exception as e:
            return MascotaController.error_response(f'Error al obtener mascotas: {str(e)}', 500)

    @staticmethod
    @mascota_bp.route('/<int:id>', methods=['GET'])
    @token_required
    def get_by_id(id):
        try:
            mascota = MascotaService.get_by_id(id)
            if not mascota:
                return MascotaController.error_response('Mascota no encontrada', 404)
            return MascotaController.success_response(mascota.to_dict())
        except Exception as e:
            return MascotaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @mascota_bp.route('', methods=['POST'])
    def create():
        try:
            data = request.get_json()
            mascota = MascotaService.create(data)
            return MascotaController.success_response(mascota.to_dict(), "Mascota creada", 201)
        except Exception as e:
            return MascotaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @mascota_bp.route('/<int:id>', methods=['PUT'])
    @token_required
    def update(id):
        try:
            data = request.get_json()
            mascota = MascotaService.update(id, data)
            if not mascota:
                return MascotaController.error_response("Mascota no encontrada", 404)
            return MascotaController.success_response(mascota.to_dict(), "Actualizada correctamente")
        except Exception as e:
            return MascotaController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @mascota_bp.route('/<int:id>', methods=['DELETE'])
    @token_required
    def delete(id):
        try:
            success = MascotaService.delete(id)
            if not success:
                return MascotaController.error_response("Mascota no encontrada", 404)
            return MascotaController.success_response(message="Mascota eliminada")
        except Exception as e:
            return MascotaController.error_response(f'Error: {str(e)}', 500)

mascota_controller = MascotaController()