USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'DW_Congresos')
BEGIN
    ALTER DATABASE DW_Congresos SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DW_Congresos;
END
GO

CREATE DATABASE DW_Congresos;
GO

USE DW_Congresos;
GO

-- =========================
-- DIMENSIONES
-- =========================

CREATE TABLE DIM_TIEMPO (
    sk_tiempo       INT IDENTITY(1,1) PRIMARY KEY,
    fecha           DATE NOT NULL UNIQUE,
    anio            INT NOT NULL,
    semestre        INT NOT NULL,
    trimestre       INT NOT NULL,
    mes             INT NOT NULL,
    nombre_mes      VARCHAR(45) NOT NULL,
    quincena        INT NOT NULL,
    semana          INT NOT NULL,
    dia             INT NOT NULL
);

CREATE TABLE DIM_PARTICIPANTE (
    sk_participante INT IDENTITY(1,1) PRIMARY KEY,
    nk_clave_part   INT NOT NULL,
    nom             VARCHAR(45) NOT NULL,
    ap_pat          VARCHAR(45) NOT NULL,
    ap_mat          VARCHAR(45) NULL,
    inst            VARCHAR(45) NOT NULL,
    tipo_part       VARCHAR(45) NOT NULL,
    nacionalidad    VARCHAR(45) NULL,
    dir             VARCHAR(45) NULL,
    grado           VARCHAR(45) NOT NULL
);

CREATE TABLE DIM_CONFERENCIA (
    sk_conferencia  INT IDENTITY(1,1) PRIMARY KEY,
    nk_clave_conf   INT NOT NULL,
    costo           FLOAT NOT NULL,
    categoria_costo VARCHAR(45) NOT NULL,
    fecha           DATE NOT NULL
);

CREATE TABLE DIM_ARTICULO (
    sk_articulo     INT IDENTITY(1,1) PRIMARY KEY,
    nk_clave_art    INT NOT NULL,
    titulo          VARCHAR(45) NOT NULL,
    nombre_autor    VARCHAR(45) NOT NULL,
    grado_autor     VARCHAR(45) NOT NULL,
    correo_autor    VARCHAR(45) NULL
);

CREATE TABLE DIM_TALLER (
    sk_taller       INT IDENTITY(1,1) PRIMARY KEY,
    nk_clave_taller INT NOT NULL,
    nombre          VARCHAR(45) NOT NULL,
    costo           FLOAT NOT NULL,
    categoria_costo VARCHAR(45) NOT NULL,
    fecha_ini       DATE NOT NULL,
    fecha_fin       DATE NOT NULL,
    duracion_dias   INT NOT NULL
);

CREATE TABLE DIM_INSTRUCTOR (
    sk_instructor    INT IDENTITY(1,1) PRIMARY KEY,
    nk_id_instructor INT NOT NULL,
    nom              VARCHAR(45) NOT NULL,
    institucion      VARCHAR(45) NOT NULL,
    grado            VARCHAR(45) NOT NULL
);

-- =========================
-- TABLAS DE HECHOS
-- =========================

CREATE TABLE FACT_INSC_CONFERENCIA (
    sk_participante   INT NOT NULL,
    sk_conferencia    INT NOT NULL,
    sk_tiempo         INT NOT NULL,
    sk_articulo       INT NOT NULL,
    costo_conferencia FLOAT NOT NULL,
    num_articulos     INT NOT NULL DEFAULT 1,
    cantidad_insc     INT NOT NULL DEFAULT 1,
    PRIMARY KEY (sk_participante, sk_conferencia, sk_tiempo),
    FOREIGN KEY (sk_participante) REFERENCES DIM_PARTICIPANTE(sk_participante),
    FOREIGN KEY (sk_conferencia) REFERENCES DIM_CONFERENCIA(sk_conferencia),
    FOREIGN KEY (sk_tiempo) REFERENCES DIM_TIEMPO(sk_tiempo),
    FOREIGN KEY (sk_articulo) REFERENCES DIM_ARTICULO(sk_articulo)
);

CREATE TABLE FACT_INSC_TALLER (
    sk_participante INT NOT NULL,
    sk_taller       INT NOT NULL,
    sk_tiempo       INT NOT NULL,
    sk_instructor   INT NOT NULL,
    costo_taller    FLOAT NOT NULL,
    duracion_dias   INT NOT NULL,
    cantidad_insc   INT NOT NULL DEFAULT 1,
    PRIMARY KEY (sk_participante, sk_taller, sk_tiempo),
    FOREIGN KEY (sk_participante) REFERENCES DIM_PARTICIPANTE(sk_participante),
    FOREIGN KEY (sk_taller) REFERENCES DIM_TALLER(sk_taller),
    FOREIGN KEY (sk_tiempo) REFERENCES DIM_TIEMPO(sk_tiempo),
    FOREIGN KEY (sk_instructor) REFERENCES DIM_INSTRUCTOR(sk_instructor)
);


select count(*) AS DIM_ARTICULO from DIM_ARTICULO;
select count(*) AS DIM_CONFERENCIA from DIM_CONFERENCIA;
select count(*) AS DIM_INSTRUCTOR from DIM_INSTRUCTOR;
select count(*) AS DIM_PARTICIPANTE from DIM_PARTICIPANTE;
select count(*) AS DIM_TALLER from DIM_TALLER;
select count(*) AS DIM_TIEMPO from DIM_TIEMPO;
select count(*) AS FACT_INSC_CONFERENCIA from FACT_INSC_CONFERENCIA;
select count(*) AS FACT_INSC_TALLER from FACT_INSC_TALLER;

select * from FACT_INSC_TALLER
