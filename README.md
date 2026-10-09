# Proyecto de Data Warehouse, ETL y Cubo OLAP

Este repositorio contiene el código, scripts y documentación del proyecto integral de diseño, construcción y análisis de un Data Warehouse. El proyecto simula el ciclo de vida completo de los datos, desde su generación aleatoria y almacenamiento transaccional, hasta su transformación y explotación analítica mediante un Cubo de Datos.

## 📋 Arquitectura y Flujo del Proyecto

El proyecto está dividido en las siguientes fases principales, detalladas en los documentos de Práctica 3 y Práctica 4:

### 1. Base de Datos Relacional (MySQL)
Como punto de partida, se diseñó e implementó una base de datos transaccional (OLTP) en MySQL. 
* **Artefacto:** Script SQL de creación de tablas, relaciones y restricciones.

### 2. Generación e Ingesta de Datos (Python)
Para poblar la base de datos con información de prueba realista, se desarrollaron dos procesos en Python:
* **Generación de Datos:** Un script de Python que utiliza librerías (como `random` o `Faker`) para crear registros sintéticos y exportarlos a archivos `.csv`.
* **Importación de Datos:** Un segundo script que utiliza la librería `pandas` para leer los archivos `.csv` generados y realizar la carga masiva de estos datos hacia la base de datos MySQL.

### 3. Creación del Data Warehouse (SQL Server)
Una vez estructurados los datos operativos, se diseñó un modelo multidimensional (esquema estrella o copo de nieve) para el almacenamiento analítico (OLAP).
* **Artefacto:** Scripts DDL en SQL Server para la creación del Data Warehouse (Tablas de Hechos y Tablas de Dimensiones).

### 4. Reglas de Negocio y Proceso ETL (Visual Studio)
La migración de datos desde MySQL hacia el Data Warehouse en SQL Server se realizó aplicando reglas de negocio específicas para la limpieza, transformación y carga de los datos.
* **Proceso ETL:** Implementado utilizando Visual Studio (SQL Server Integration Services - SSIS).
* **Reglas de negocio:** Filtrado de datos nulos, estandarización de formatos (fechas, textos), y generación de llaves subrogadas para las dimensiones.

### 5. Cubo de Datos y KPIs 
Para la explotación de la información y la toma de decisiones, se construyó un Cubo OLAP sobre el Data Warehouse.
* **Métricas y KPIs:** Definición de indicadores clave de rendimiento.
* **Análisis:** El cubo permite realizar cruces de información complejos (drill-down, roll-up) para analizar tendencias históricas de manera eficiente.

---

## 🛠️ Tecnologías Utilizadas

* **Bases de Datos:** MySQL (OLTP), SQL Server (OLAP / Data Warehouse).
* **Lenguajes:** SQL, Python.
* **Librerías de Python:** `pandas`, librerías de generación random/faker.
* **Herramientas ETL/BI:** Visual Studio (SSIS), SQL Server Analysis Services (SSAS) para el cubo de datos.

---

## 📌 Conclusiones

Este proyecto demuestra la implementación exitosa de una arquitectura de datos completa. A través del proceso ETL, se logró transformar datos transaccionales crudos en información analítica valiosa y estructurada. La creación final del Cubo OLAP y la definición de KPIs permiten a los usuarios finales (tomadores de decisiones) consultar métricas complejas con alta velocidad y flexibilidad, cumpliendo con el objetivo principal de las herramientas de Business Intelligence.
