import os
from flask import Flask
from config import Config
from models import db, Admin
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "warning"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(admin_id):
        return Admin.query.get(int(admin_id))

    with app.app_context():
        # Import and register blueprints
        from routes.main import main_bp
        from routes.shop import shop_bp
        from routes.cart import cart_bp
        from routes.admin import admin_bp
        from routes.auth import auth_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(shop_bp)
        app.register_blueprint(cart_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        # Create database tables
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
