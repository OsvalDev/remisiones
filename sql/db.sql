CREATE TABLE USUARIO(
    id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    psw VARCHAR(200) NOT NULL,
    activo BOOLEAN  NOT NULL DEFAULT 1,
    PRIMARY KEY(id)
);

CREATE TABLE AREA(
    id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE USUARIO_AREA(
    idUsuario INT NOT NULL,
    idArea INT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY(idArea, idUsuario, fecha),
    FOREIGN KEY(idArea) REFERENCES AREA(id),
    FOREIGN KEY(idUsuario) REFERENCES USUARIO(id)
);

CREATE TABLE PERMISO(
    id INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE AREA_PERMISO(
    idArea INT(11) NOT NULL,
    idPermiso INT(11) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY(idArea, idPermiso, fecha),
    FOREIGN KEY(idArea) REFERENCES AREA(id),
    FOREIGN KEY(idPermiso) REFERENCES PERMISO(id)
);

CREATE TABLE CLIENTE(
    id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(400) NOT NULL,
    saldoBonificado float NOT NULL DEFAULT 0,
    PRIMARY KEY(id)
);

CREATE TABLE ESTATUS(
    id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE REMISION(
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    piezas INT NOT NULL,
    importeRemisionado FLOAT NOT NULL,
    importeFacturado FLOAT NOT NULL,
    fechaCompromisoCliente DATE DEFAULT NULL,
    estatus INT NOT NULL DEFAULT 1,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    cliente INT NOT NULL,
    saldoAFavor FLOAT NOT NULL,
    numFactura VARCHAR(100) NOT NULL,
    PRIMARY KEY(numCompra, numRemision),
    FOREIGN KEY(cliente) REFERENCES CLIENTE(id),
    FOREIGN KEY(estatus) REFERENCES ESTATUS(id)
);

CREATE TABLE NOTAREMISION(
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    contenido VARCHAR(500) NOT NULL,
    usuario INT NOT NULL,
    PRIMARY KEY(numCompra, numRemision, fecha),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE NOTAENTREGA(
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    contenido VARCHAR(500) NOT NULL,
    usuario INT NOT NULL,
    PRIMARY KEY(numCompra, numRemision, fecha),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE DEVOLUCION(
    id INT AUTO_INCREMENT,
    descripcion VARCHAR(500) NOT NULL,
    cantidadBonificada FLOAT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision)
);

CREATE TABLE PROCESO(
    id INT NOT NULL AUTO_INCREMENT,
    accion VARCHAR(50) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    fechaCompromiso DATE DEFAULT NULL,
    fechaConcluido DATE DEFAULT NULL,
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    usuario INT NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE NOTIFICANTEENTREGA(
    id INT NOT NULL,
    usuario INT NOT NULL,
    paqueteria VARCHAR(200),
    PRIMARY KEY(id, usuario),
    FOREIGN KEY(id) REFERENCES PROCESO(id),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE NOTA(
    id INT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    contenido VARCHAR(500) NOT NULL,
    usuario INT NOT NULL,
    PRIMARY KEY(id, fecha),
    FOREIGN KEY(id) REFERENCES PROCESO(id),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

CREATE TABLE PAGO(
    id INT NOT NULL AUTO_INCREMENT,
    cantidad FLOAT NOT NULL,
    pagoPersona VARCHAR(500) NOT NULL,
    comprobante VARCHAR(500) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    responsable INT NOT NULL,
    numRemision VARCHAR(100) NOT NULL,
    numCompra VARCHAR(100) NOT NULL,
    confirmante INT,
    fechaConfirmacion DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY(numCompra, numRemision) REFERENCES REMISION(numCompra, numRemision),
    FOREIGN KEY(responsable) REFERENCES USUARIO(id),
    FOREIGN KEY(confirmante) REFERENCES USUARIO(id)
);

CREATE TABLE NOTAPAGO(
    id INT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    contenido VARCHAR(500) NOT NULL,
    usuario INT NOT NULL,
    PRIMARY KEY(id, fecha),
    FOREIGN KEY(id) REFERENCES PAGO(id),
    FOREIGN KEY(usuario) REFERENCES USUARIO(id)
);

INSERT INTO AREA(id, nombre) VALUES 
(1, 'ventas'),
(2, 'logistica'),
(3, 'surtimiento'),
(4, 'chofer'),
(5, 'admin'),
(6, 'cuentasCobrar'),
(7, 'gerente');

INSERT INTO PERMISO(id, accion) VALUES
(1, 'agregarUsuario'),
(2, 'crearRemision'),
(3, 'agregarCliente'),
(4, 'editarRemision'),
(5, 'seguimientoSurtimiento'),
(6, 'seguimientoLogistica'),
(7, 'asignarChofer'),
(8, 'confirmarEntrega'),
(9, 'registrarPago'),
(10, 'confirmarPago'),
(11, 'registrarDevolucion'),
(12, 'autorizar');

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
(5, 12),
(6, 10),
(6, 12)
(7, 1);

INSERT INTO ESTATUS VALUES
(1, 'Sin comenzar'),
(2, 'Surtimiento'),
(3, 'Logistica'),
(4, 'Entrega confirmada'),
(5, 'Entregado'),
(6, 'Pagado'),
(7, 'Finalizado');