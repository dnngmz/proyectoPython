from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registrar blueprints
    from app.controllers.user_controller import user_bp
    from app.controllers.note_controller import note_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.mascota_controller import mascota_bp
    from app.controllers.especialidad_controller import especialidad_bp
    from app.controllers.doctor_controller import doctor_bp
    from app.controllers.cita_controller import cita_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(note_bp, url_prefix='/api/notes')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(cliente_bp, url_prefix = '/api/clientes')
    app.register_blueprint(mascota_bp, url_prefix = '/api/mascotas')
    app.register_blueprint(especialidad_bp, url_prefix = '/api/especialidades')
    app.register_blueprint(doctor_bp, url_prefix = '/api/doctores')
    app.register_blueprint(cita_bp, url_prefix = '/api/citas')

    return app
