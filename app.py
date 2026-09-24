from flask import Flask
from club_deportivo.routes import deportes_bp, canchas_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(deportes_bp)
    app.register_blueprint(canchas_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)