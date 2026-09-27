from flask import Flask

from club_deportivo.rutas.deportes import deportes_bp
from club_deportivo.rutas.canchas import canchas_bp
from club_deportivo.rutas.socios import socios_bp
from club_deportivo.rutas.reservas import reservas_bp


def create_app():

    app = Flask(__name__)

    app.register_blueprint(deportes_bp)
    app.register_blueprint(canchas_bp)
    app.register_blueprint(socios_bp)
    app.register_blueprint(reservas_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
