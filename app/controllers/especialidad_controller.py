from flask import Blueprint, request
from app.services.especialidad_service import EspecialidadService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required

especialidad_bp = Blueprint('especialidades', __name__)
especialidad_service = EspecialidadService()

class EspecialidadController(BaseController):
    def __init__(self):
        super().__init__(especialidad_service)

    @staticmethod
    @especialidad_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        try:
            especialidades = EspecialidadService.get_all()
            return EspecialidadController.success_response(
                data=[e.to_dict() for e in especialidades],
                message=f'Se encontraron {len(especialidades)} especialidades'
            )
        except Exception as e:
            return EspecialidadController.error_response(f'Error al obtener especialidades: {str(e)}', 500)

    @staticmethod
    @especialidad_bp.route('/<int:id>', methods=['GET'])
    @token_required
    def get_by_id(id):
        try:
            especialidad = EspecialidadService.get_by_id(id)
            if not especialidad:
                return EspecialidadController.error_response('Especialidad no encontrada', 404)
            return EspecialidadController.success_response(especialidad.to_dict())
        except Exception as e:
            return EspecialidadController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @especialidad_bp.route('', methods=['POST'])
    def create():
        try:
            data = request.get_json()
            especialidad = EspecialidadService.create(data)
            return EspecialidadController.success_response(especialidad.to_dict(), "Especialidad creada", 201)
        except Exception as e:
            return EspecialidadController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @especialidad_bp.route('/<int:id>', methods=['PUT'])
    @token_required
    def update(id):
        try:
            data = request.get_json()
            especialidad = EspecialidadService.update(id, data)
            if not especialidad:
                return EspecialidadController.error_response("Especialidad no encontrada", 404)
            return EspecialidadController.success_response(especialidad.to_dict(), "Actualizada correctamente")
        except Exception as e:
            return EspecialidadController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @especialidad_bp.route('/<int:id>', methods=['DELETE'])
    @token_required
    def delete(id):
        try:
            success = EspecialidadService.delete(id)
            if not success:
                return EspecialidadController.error_response("Especialidad no encontrada", 404)
            return EspecialidadController.success_response(message="Especialidad eliminada")
        except Exception as e:
            return EspecialidadController.error_response(f'Error: {str(e)}', 500)

especialidad_controller = EspecialidadController()