Markdown
[![](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org)
[![](https://img.shields.io/badge/Domain--Driven-Design-orange.svg?style=flat)](https://en.wikipedia.org/wiki/Domain-driven_design)
[![](https://img.shields.io/badge/Pytest-Passing-green.svg?style=flat&logo=pytest)](https://docs.pytest.org)
[![](https://img.shields.io/badge/Scenarios-15%2F15-success.svg?style=flat)](https://github.com)

# TechStore - Sistema de Gestion de Pedidos (Unidad 4)

Sistema backend desarrollado en Python bajo principios de Domain-Driven Design (DDD) para la gestion y validacion de reglas de negocio en el flujo de pedidos de una tienda de tecnologia. El proyecto implementa control de estados, validaciones de clientes y catalogos, calculos financieros precisos y una suite completa de pruebas unitarias y de integracion de escenarios.

## Estructura del Proyecto

El proyecto sigue una separacion clara entre las entidades del dominio de negocio, la carga de datos (fixtures) y los scripts de prueba:

```text
Proyecto-U4/
│
├── app/
│   ├── __init__.py
│   ├── domain.py            # Modelos de dominio (dataclasses), Value Objects (Money), Reglas y Excepciones
│   └── test_escenarios.py   # Suite de validacion de los 15 escenarios oficiales de negocio (E01-E15)
│
├── datos/
│   ├── clientes.csv         # Fixtures de clientes (estado activo/inactivo, membresia VIP)
│   ├── productos.csv        # Catalogo de productos y precios unitarios en MXN
│   ├── pedidos.csv          # Cabeceras iniciales de los pedidos del sistema
│   └── detalle_pedidos.csv  # Items y cantidades asociadas a cada pedido
│
├── cargar_csv.py            # Cargador de fixtures e hidratacion relacional de entidades desde CSV
├── main.py                  # Script ejecutable principal para la evaluacion de los 15 escenarios
└── test_app.py              # Suite de pruebas unitarias implementadas con Pytest
Reglas de Negocio Implementadas
El sistema valida de forma estricta las siguientes restricciones y comportamientos de dominio:

Gestion de Estados del Pedido
Ciclo de vida controlado mediante una maquina de estados (DRAFT, CONFIRMED, SHIPPED, DELIVERED, RETURNED, CANCELLED) con transiciones permitidas y prohibidas.

Validacion de Clientes
Los pedidos solo pueden ser confirmados si el cliente asociado se encuentra en estado activo. Los clientes inactivos generan un rechazo de dominio (InactiveCustomerError).

Limites de Articulos
Restriccion en la cantidad maxima de unidades permitidas por item o pedido para evitar saturaciones o abusos de stock (OrderItemLimitExceeded).

Calculos Financieros y Descuentos
Uso de la clase Decimal para garantizar precision absoluta en montos monetarios en moneda nacional (MXN).

Aplicacion automatica de descuentos VIP (20%) cuando el cliente o el pedido cumplen con la regla de membresia.

Manejo de promociones activas e impuestos.

Control de Envios y Devoluciones
Todo pedido en estado CONFIRMED requiere obligatoriamente un numero de guia de envio valido para transicionar a SHIPPED. Se permite la gestion de entregas y devoluciones posteriores.

Requisitos del Sistema
Python version 3.10 o superior.

Libreria de pruebas Pytest (opcional, requerida unicamente si se ejecutan las pruebas unitarias independientes).

Guia de Ejecucion
1. Clonar o descargar el repositorio
Asegurate de ubicarte en la carpeta raiz del proyecto (Proyecto-U4) en tu terminal local.

2. Ejecutar los Escenarios de Negocio (E01 a E15)
Para correr la validacion oficial de los 15 escenarios que evaluan el comportamiento integrado del sistema frente a los fixtures, ejecuta:

Bash
python main.py
Una ejecucion exitosa mostrara el siguiente resultado en consola:

Plaintext
--- Evaluando reglas de negocio en escenarios ---
  E01: [OK  ]    ->   Obtenido: 10%       | Esperado: 10%
  E02: [OK  ]    ->   Obtenido: 0%        | Esperado: 0%
  E03: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E04: [OK  ]    ->   Obtenido: 0%        | Esperado: 0%
  E05: [OK  ]    ->   Obtenido: 5%        | Esperado: 5%
  E06: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E07: [OK  ]    ->   Obtenido: exito     | Esperado: exito
  E08: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E09: [OK  ]    ->   Obtenido: 0%        | Esperado: 0%
  E10: [OK  ]    ->   Obtenido: 0%        | Esperado: 0%
  E11: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E12: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E13: [OK  ]    ->   Obtenido: rechazo   | Esperado: rechazo
  E14: [OK  ]    ->   Obtenido: RETURNED  | Esperado: RETURNED
  E15: [OK  ]    ->   Obtenido: DELIVERED | Esperado: DELIVERED

Resultado final: 15/15 escenarios correctos
3. Ejecutar la Suite de Pruebas Unitarias (Pytest)
Para validar el comportamiento aislado de las clases de dominio, excepciones y casos borde mediante pytest, ejecuta:

Bash
pytest -v
Decisiones Tecnicas y Patrones
Inmutabilidad y Tipado: Uso intensivo de dataclasses con validaciones en los constructores (__post_init__) para mantener la integridad de los datos de dominio desde el primer instante.

Manejo de Excepciones de Dominio: Jerarquia limpia de excepciones personalizadas (DomainException y subclases especificas) que permiten al sistema rechazar operaciones invalidas de manera controlada y predecible.

Separacion de Infraestructura y Dominio: Los datos tabulares planos de los archivos CSV son leidos y transformados limpiamente a entidades ricas de dominio mediante el cargador desacoplado (cargar_csv.py).
