from flask import Blueprint, request
from app.services.doctor_service import DoctorService
from app.controllers.base_controller import BaseController
from app.utils.auth_decorators import token_required

doctor_bp = Blueprint('doctores', __name__)
doctor_service = DoctorService()

class DoctorController(BaseController):
    def __init__(self):
        super().__init__(doctor_service)

    @staticmethod
    @doctor_bp.route('', methods=['GET'])
    @token_required
    def get_all():
        try:
            doctores = DoctorService.get_all()
            return DoctorController.success_response(
                data=[d.to_dict() for d in doctores],
                message=f'Se encontraron {len(doctores)} doctores'
            )
        except Exception as e:
            return DoctorController.error_response(f'Error al obtener doctores: {str(e)}', 500)

    @staticmethod
    @doctor_bp.route('/<int:id>', methods=['GET'])
    @token_required
    def get_by_id(id):
        try:
            doctor = DoctorService.get_by_id(id)
            if not doctor:
                return DoctorController.error_response('Doctor no encontrado', 404)
            return DoctorController.success_response(doctor.to_dict())
        except Exception as e:
            return DoctorController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @doctor_bp.route('', methods=['POST'])
    def create():
        try:
            data = request.get_json()
            doctor = DoctorService.create(data)
            return DoctorController.success_response(doctor.to_dict(), "Doctor creado", 201)
        except Exception as e:
            return DoctorController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @doctor_bp.route('/<int:id>', methods=['PUT'])
    @token_required
    def update(id):
        try:
            data = request.get_json()
            doctor = DoctorService.update(id, data)
            if not doctor:
                return DoctorController.error_response("Doctor no encontrado", 404)
            return DoctorController.success_response(doctor.to_dict(), "Actualizado correctamente")
        except Exception as e:
            return DoctorController.error_response(f'Error: {str(e)}', 500)

    @staticmethod
    @doctor_bp.route('/<int:id>', methods=['DELETE'])
    @token_required
    def delete(id):
        try:
            success = DoctorService.delete(id)
            if not success:
                return DoctorController.error_response("Doctor no encontrado", 404)
            return DoctorController.success_response(message="Doctor eliminado")
        except Exception as e:
            return DoctorController.error_response(f'Error: {str(e)}', 500)

doctor_controller = DoctorController()