import os
from flask import Flask, render_template
from config import Config

def create_app():
    # Absolute paths required for Vercel serverless runtime
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    # Register Blueprints
    from routes.public import public_bp
    from routes.admin import admin_bp
    from routes.kamar import admin_kamar_bp
    from routes.penghuni import admin_penghuni_bp
    from routes.sewa import admin_sewa_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_kamar_bp)
    app.register_blueprint(admin_penghuni_bp)
    app.register_blueprint(admin_sewa_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
