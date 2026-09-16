/* Creación de la base de datos */
DROP DATABASE IF EXISTS club_deportivo;

CREATE DATABASE club_deportivo;

USE club_deportivo;

/* Creación de tablas */
CREATE TABLE deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_canchas_deporte
        FOREIGN KEY (id_deporte)
        REFERENCES deportes(id),

    CONSTRAINT chk_canchas_precio
        CHECK (precio_hora > 0)
);

CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(75) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'finalizada')
        NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,

    CONSTRAINT fk_reservas_socio
        FOREIGN KEY (id_socio)
        REFERENCES socios(id),

    CONSTRAINT fk_reservas_cancha
        FOREIGN KEY (id_cancha)
        REFERENCES canchas(id),

    CONSTRAINT chk_reservas_fechas
        CHECK (fecha_hora_fin > fecha_hora_inicio),

    CONSTRAINT chk_reservas_precio_hora
        CHECK (precio_hora > 0),

    CONSTRAINT chk_reservas_precio_total
        CHECK (precio_total >= 0)
);

/* Carga de datos de prueba */

INSERT INTO deportes (nombre)
VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');

INSERT INTO canchas (
    nombre,
    id_deporte,
    precio_hora,
    techada,
    activa
)
VALUES
    ('Cancha Fútbol 1', 1, 1000000, FALSE, TRUE),
    ('Cancha Fútbol 2', 1, 1200000, TRUE, TRUE),
    ('Cancha Tenis 1', 2, 800000, TRUE, TRUE),
    ('Cancha Pádel 1', 3, 1500000, TRUE, TRUE);

INSERT INTO socios (
    nombre,
    email,
    activo
)
VALUES
    ('Juan Pérez', 'juan.perez@email.com', TRUE),
    ('María López', 'maria.lopez@email.com', TRUE),
    ('Pedro Gómez', 'pedro.gomez@email.com', TRUE),
    ('Ana Rodríguez', 'ana.rodriguez@email.com', TRUE);