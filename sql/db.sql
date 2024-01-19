CREATE TABLE USUARIO(
    id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    psw VARCHAR(200) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE AREA(
    id INT AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE USUARIO_AREA(
    idUsuario INT,
    idArea INT,
    fecha TIMESTAMP,
    PRIMARY KEY(idArea, idUsuario, fecha),
    FOREIGN KEY(idArea) REFERENCES AREA(id),
    FOREIGN KEY(idUsuario) REFERENCES USUARIO(id)
);

CREATE TABLE PERMISO(
    id INT AUTO_INCREMENT,
    accion VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE AREA_PERMISO(
    idArea INT,
    idPermiso INT,
    fecha TIMESTAMP,
    PRIMARY KEY(idArea, idPermiso, fecha),
    FOREIGN KEY(idArea) REFERENCES AREA(id),
    FOREIGN KEY(idPermiso) REFERENCES PERMISO(id)
);

CREATE TABLE CLIENTE(
    id INT,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(400) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    saldoBonificado INT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE REMISION(
    numRemision VARCHAR(100),
    numCompra VARCHAR(100),
    piezas INT NOT NULL,
    importeRemisionado INT NOT NULL,
    importeFacturado INT NOT NULL,
    fechaCompromisoCliente DATETIME NOT NULL,
    fecha TIMESTAMP,
    cliente INT NOT NULL,
    saldoAFavor INT NOT NULL,
    PRIMARY KEY(numCompra, numRemision),
    FOREIGN KEY(cliente) REFERENCES CLIENTE(id)
);

CREATE TABLE DEVOLUCION(
    id INT,
    descripcion VARCHAR(500) NOT NULL,
    cantidadBonificada INT NOT NULL,
    fecha TIMESTAMP,
    numRemision VARCHAR(100),
    numCompra VARCHAR(100),
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision)
);

CREATE TABLE PROCESO(
    id INT AUTO_INCREMENT,
    accion VARCHAR(50) NOT NULL,
    fecha TIMESTAMP,
    fechaCompromiso DATE NOT NULL,
    concluido BOOLEAN NOT NULL,
    numRemision VARCHAR(100),
    numCompra VARCHAR(100),
    usuario INT NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE NOTA(
    id INT,
    fecha TIMESTAMP,
    contenido VARCHAR(500) NOT NULL,
    PRIMARY KEY(id, fecha),
    FOREIGN KEY(id) REFERENCES PROCESO(id)
);

CREATE TABLE PAGO(
    id INT AUTO_INCREMENT,
    cantidad INT NOT NULL,
    pagoPersona VARCHAR(500) NOT NULL,
    confirmado BOOLEAN NOT NULL,
    comprobante VARCHAR(500) NOT NULL,
    fecha TIMESTAMP,
    proceso INT NOT NULL,
    responsable INT NOT NULL,
    numRemision VARCHAR(100),
    numCompra VARCHAR(100),
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(responsable) REFERENCES USUARIO(id),
    FOREIGN KEY(proceso) REFERENCES PROCESO(id)
);

CREATE TABLE NOTAPAGO(
    id INT,
    fecha TIMESTAMP,
    contenido VARCHAR(500) NOT NULL,
    PRIMARY KEY(id, fecha),
    FOREIGN KEY(id) REFERENCES PAGO(id)
);

INSERT INTO AREA(nombre) VALUES 
('ventas'),
('logistica'),
('surtimiento'),
('chofer'),
('admin'),
('cuentasCobrar'),
('gerente');

INSERT INTO PERMISO(accion) VALUES
('agregarUsuario'),
('crearRemision'),
('agregarCliente'),
('editarRemision'),
('seguimientoSurtimiento'),
('seguimientoLogistica'),
('asignarChofer'),
('confirmarEntrega'),
('registrarPago'),
('confirmarPago'),
('registrarDevolucion');

INSERT INTO AREA_PERMISO(idArea, idPermiso) VALUES
(1, 2),
(1, 3),
(1, 4),
(1, 11),
(2, 6),
(2, 7),
(2, 8),
(3, 5),
(4, 9),
(5, 1),
(5, 2),
(5, 3),
(5, 4),
(5, 5),
(5, 6),
(5, 7),
(5, 8),
(5, 9),
(5, 10),
(5, 11),
(6, 10),
(7, 1);