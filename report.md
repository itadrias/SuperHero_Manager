# 🛡️ S.H.M. - SuperHero Manager

> **CLASIFICACIÓN:** TOP SECRET / SOLO PARA OJOS DEL COMANDANTE  
> **ESTADO:** OPERATIVO  
> **CODENAME:** "Project Avenger"

![Python](https://img.shields.io/badge/CORE-PYTHON_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kivy](https://img.shields.io/badge/INTERFACE-KIVY_2.3-FFD54F?style=for-the-badge&logo=kivy&logoColor=black)
![License](https://img.shields.io/badge/LICENSE-CLASSIFIED-red?style=for-the-badge)

Bienvenido a la consola de administración **SuperHero Manager**. Esta herramienta ha sido diseñada para coordinar, desplegar y gestionar activos súper-humanos en operaciones de campo.

---

## 🌐 Informe de Misión (El Dominio)

Este proyecto simula la gestión interna de una **Agencia de Superhéroes**. Aunque el tema parece un juego, el sistema resuelve problemas reales de logística y planificación. Elegí este dominio porque ofrece retos de programación mucho más interesantes que un inventario común.

### ¿Por qué este tema?

1. **Héroes como Recursos Únicos:**
Cada héroe es único y su tiempo es limitado. A diferencia de una caja de productos, no puedes usar a la misma persona en dos lugares a la vez. Esto requiere un control de agenda preciso para evitar conflictos.
2. **Reglas del Juego (Restricciones):**
No basta con agrupar gente. El sistema debe ser inteligente para entender reglas complejas:
* **Equipo necesario:** Algunos héroes no funcionan sin sus herramientas específicas.
* **Problemas de equipo:** Hay héroes que simplemente no pueden trabajar juntos.


3. **Interfaz Visual:**
Un sistema de héroes necesita verse bien. El uso de **Kivy** está justificado para poder mostrar perfiles, barras de poder y esquemas de misiones de una manera gráfica y fácil de entender, algo que una consola de texto no permite.

**El Propósito Real (Más allá del Dominio):**
A nivel académico y de ingeniería, el programa resuelve un problema clásico de gestión: asignar recursos limitados a tareas bajo un sistema estricto de reglas. El usuario interactúa con un sistema subyacente que calcula capacidades, detecta incompatibilidades y comprueba calendarios. Esta mezcla convierte a la aplicación en un simulador de planificación funcional disfrazado bajo una capa narrativa. El tema de los superhéroes no es puramente decorativo; es el vehículo perfecto para representar de forma intuitiva conceptos de exclusividad de recursos, bloqueo por agenda y dependencias de variables.

---

## ⚙️ Mecánicas y Funcionamiento Interno

El sistema se apoya en dos módulos lógicos principales ubicados en la carpeta `widgets/` que garantizan el correcto funcionamiento de la agencia:

### 1. Sistema de Control Temporal (`checker.py` y `date_selector.py`):

Este módulo es el responsable de gestionar la agenda y disponibilidad de los efectivos.

* **Validación de Conflictos (`check_overlapping`):** Analiza la línea de tiempo propuesta. Si se intenta asignar a un héroe que ya se encuentra desplegado en otra misión durante esas fechas, el sistema consulta la base de datos y bloquea la operación para evitar duplicidad. No basta con comparar fechas como texto; el uso de objetos `datetime` en el selector permite medir intervalos exactos y detectar cruces precisos.
* **Cálculo de Disponibilidad (`next_available`):** En caso de conflicto, esta función recursiva procesa la agenda para calcular automáticamente cuál es el próximo intervalo de tiempo en el que **todo** el equipo seleccionado estará disponible simultáneamente.

### 2. Sistema de Reglas y Restricciones (`restrictions.py`)

Además de la disponibilidad, es crucial validar la viabilidad operativa del equipo. Este módulo asegura que se cumplan los requisitos de la misión evitando que el usuario persista estados inconsistentes. El programa implementa un patrón de **"validación antes de persistir"**: no se escribe en la base de datos hasta que atributos, restricciones y fechas hayan sido aprobados en cadena.

* **Verificación de Atributos:** Suma las estadísticas de los héroes seleccionados. Si el equipo no alcanza los niveles requeridos (ej. Fuerza, Sigilo) para la misión, el despliegue es rechazado.
* **Lógica de Compatibilidad Múltiple:** Evalúa de forma integral las combinaciones para evitar falsos positivos donde una regla anule a otra.
* **Requisitos de Equipo (Required):** Valida dependencias técnicas; ciertos especialistas requieren llevar equipamiento específico.
* **Restricciones de Personal (Forbidden):** Implementa reglas de exclusión para prevenir que héroes incompatibles trabajen juntos.



### 📋 Tabla de Sinergias (Equipamiento Requerido)

Lista de héroes que necesitan ítems específicos para operar al 100% de su capacidad.

| Héroe | Requiere | Razón |
| --- | --- | --- |
| **Sentinel** | Chaleco Balístico | Necesario para compensar su baja resistencia natural. |
| **Cósmico** | Ancla Cibernética | Estabiliza su presencia física y evita desintegración dimensional. |
| **Raptor** | Gancho de Agarre | Indispensable para realizar giros cerrados en vuelo a alta velocidad. |
| **Tecnópata** | Potenciador Neuronal | Protege su mente del daño al procesar múltiples realidades. |
| **Comandante** | Auriculares | Canal vital y encriptado para comandar al escuadrón. |
| **Juggernaut** | Suministros | Su metabolismo acelerado exige ingesta calórica constante. |
| **Velocista** | Botas Veloces | Protege los pies de la fricción térmica a velocidades Mach. |
| **Campeón** | Blasón de Guerra | Símbolo indispensable de su honor; fuente de su moral. |

### 🚫 Tabla de Prohibiciones:

Lista de incompatibilidades entre agentes y recursos por razones de seguridad o física.

| Héroe | Incompatible con | Razón |
| --- | --- | --- |
| **Celestial** | Juggernaut | El peso excesivo del objetivo impide maniobras aéreas conjuntas. |
| **Sentinel** | Juego de Ganzúas | El sigilo viola su código de honor y combate frontal. |
| **Cósmico** | Suministros, Auriculares | Su radiación corrompe materia orgánica e interfiere señales de radio. |
| **Radiante** | Ganzúas, Kit Mascarada | Su bio-luminiscencia permanente arruina cualquier intento de sigilo. |
| **Atlante** | Dragón, Drones | Conflicto elemental (Agua/Fuego); la humedad cortocircuita drones. |
| **Dragón** | Atlante, Chaleco | Conflicto elemental; calor extremo derrite fibras balísticas estándar. |
| **Raptor** | Juggernaut | Objetivo terrestre demasiado lento para coordinar caza aérea. |
| **Tecnópata** | Radiante | La luz intensa satura su cortex visual, impidiendo proyecciones. |
| **Comandante** | Cósmico | La interferencia estática impide la emisión de órdenes claras. |
| **Juggernaut** | Botas, Gancho | Su masa descomunal destroza equipo ligero o soportes de agarre. |
| **Velocista** | Chaleco, Juggernaut | Equipo rígido limita aerodinámica; Juggernaut retrasa el avance. |

### ⚔️ Tabla de Requisitos para Misiones:

Ciertas operaciones de campo exigen especialistas o equipos concretos para ser autorizadas:

| Misión | Requisito | Razón |
| --- | --- | --- |
| **Vigilancia en Cárcel** | Juggernaut | Indispensable para contención física de alta seguridad. |
| **Actividad Sospechosa** | Comandante | Necesario para análisis táctico de patrones criminales. |
| **Sabotaje Industrial** | Tecnópata | Único capaz de contrarrestar amenazas tecnológicas. |
| **Escolta VIP** | Sentinel | Se requiere su perfil de guardaespaldas incorruptible. |
| **Robo en Museo** | Kit de Mascarada | Operación encubierta; el anonimato es prioritario. |
| **Rescate por Secuestro** | Auriculares | Comunicación constante vital para coordinación. |
| **Villano (Boss)** | Campeón | Se requiere poder de nivel "Divino" para el enfrentamiento. |
| **Banda Criminal** | Suministros | Combates prolongados requieren reabastecimiento. |
| **Ataque a Base Enemiga** | Kit de Mascarada | Infiltración profunda en territorio hostil. |

---

## 📊 Sistema de Métricas y Tipología de Misiones

### Evaluación de Activos (Chart de Habilidades)

Cada activo de la agencia es evaluado mediante un sistema hexaxial. Al seleccionar un equipo, el sistema calcula en tiempo real un **vector de capacidad conjunta** sumando los atributos individuales de cada héroe. Estos 6 pilares determinan el éxito de la operación:

* **Fuerza:** Potencia de combate bruto.
* **Inteligencia:** Capacidad táctica y resolución tecnológica.
* **Sigilo:** Infiltración y operaciones encubiertas.
* **Carisma:** Diplomacia y control de masas.
* **Movilidad:** Velocidad de respuesta y alcance.
* **Resistencia:** Durabilidad operativa bajo presión/ataques.

La interfaz visualiza estos datos mediante un **Gráfico de Radar** (`chart.py`), permitiendo al comandante evaluar de un vistazo si el equipo está equilibrado. Como decisión de diseño, este gráfico no solo dibuja puntos: traduce las estadísticas acumuladas en una figura geométrica interpretable que se superpone con los requisitos de la misión. Es una solución infinitamente más expresiva que una simple lista de números, permitiendo comparar la viabilidad del equipo al instante.

### Tipología de Operaciones

El sistema clasifica las operaciones de campo en dos categorías estratégicas, cada una con su propio set de eventos predefinidos adaptados al dominio:

1. **Patrullar (Operaciones Preventivas):**
Misiones rutinarias de bajo a medio riesgo diseñadas para mantener el orden.
* *Ejemplos:* "Vigilancia en Cárcel", "Escolta VIP", "Rescate por Secuestro".
* *Enfoque:* Suelen requerir altos niveles de **Movilidad** y **Carisma** para cubrir terreno.


2. **Luchar (Operaciones Reactivas):**
Eventos críticos de alto riesgo que requieren intervención directa contra amenazas confirmadas.
* *Ejemplos:* "Enfrentamiento a Villanos", "Amenazas Desconocidas", "Ataque a la Base".
* *Enfoque:* Demandan picos extremos de **Fuerza** y **Resistencia**, con requisitos estrictos de equipamiento especializado.


3. **Añadir (Protocolos Personalizados):**
Esta funcionalidad otorga flexibilidad táctica total al mando. Permite diseñar y registrar situaciones no contempladas en los escenarios estándar.
* *Libertad Operativa:* El usuario tiene control total para definir el nombre y los parámetros temporales del evento.
* *Integración de Recursos:* Aunque el evento es nuevo, se construye utilizando el **pool de recursos del dominio** (héroes y artefactos existentes). El sistema aplicará las mismas matrices de validación (`checkers`) para asegurar que estos recursos asignados manualmente sean compatibles y estén disponibles.



---

## 🖥️ Guía de la Interfaz y Flujos de Uso

El flujo de uso de la interfaz está guiado intencionalmente para reducir errores. El sistema obliga a una secuencia ordenada (Misión -> Equipo -> Fecha -> Confirmar) para evitar estados inconsistentes.

### Selector de Héroes (`hero_selector.py` y `panel.py`):

Aquí es donde se elige al equipo encargado de la misión que se desea planificar.

* **Click Izquierdo (Reclutar):** Activa al héroe para la misión actual. Verás el **Gráfico de Radar** actualizarse en tiempo real sumando sus estadísticas. El borde animado indica su estado activo dentro del equipo.
* **Click Derecho (Ver Archivo):** Accede al expediente del héroe (`InfoPanel`), revelando su biografía y estadísticas base de manera contextual. Esta separación entre hover/click derecho para información y click izquierdo para acción evita que el usuario confunda consultas con despliegues.

### Ejemplos Prácticos de Flujo Operativo:

**Caso 1: Misión de Rutina (Patrulla)**

1. **Categoría:** Entra al menú principal y selecciona la categoría de patrulla.
2. **Objetivo:** Elige, por ejemplo, "Rescate por Secuestro". Lee el panel informativo para entender que necesitas altos niveles de movilidad.
3. **Asignación:** Selecciona héroes rápidos y el ítem obligatorio (Auriculares para coordinación). El gráfico validará el equilibrio.
4. **Fecha y Confirmación:** Define el rango horario. Si los algoritmos aprueban las restricciones y la agenda, la operación se confirma y persiste.

**Caso 2: Creación de Protocolo Personalizado (Añadir)**

1. **Categoría:** Accede a la opción de añadir nuevo evento.
2. **Definición:** Escribe un nombre táctico corto y claro.
3. **Gestión Manual:** Asigna recursos verificando visualmente que no existan incompatibilidades entre ellos.
4. **Despliegue:** Introduce el intervalo horario libre y guarda la misión en la base de datos.

### Vista de Eventos (`events_view.py`):

Un listado cronológico de todas las operaciones activas, que funciona como el panel de control de la agencia.

* Las tarjetas (**Ver Detalles**) muestran el estado de la misión y los agentes asignados.
* Interacción fluida para cancelar operaciones (**Eliminar**) y liberar recursos inmediatamente, disparando un reordenamiento cronológico automático en el backend.

---

## 🛠️ Tecnologías, Arquitectura y Dificultades Técnicas

El sistema está construido sobre **Python 3** utilizando una arquitectura altamente modular basada en archivos JSON para máxima portabilidad. Una de las decisiones arquitectónicas clave fue **separar la lógica de los datos**: los héroes, ítems y reglas no están *hardcodeados*, sino encriptados en archivos `.json`. Esto estabiliza el código fuente permitiendo que el contenido sea fácilmente escalable y editable.

### Árbol de Directorios / Blueprints:

```text
Project/
├── 📁 images/               # Archivos de identidad visual (Héroes/Items)
├── 📁 json/                 # Base de Datos Encriptada (JSON)
│   ├── events.json          # Registro de operaciones y persistencia
│   ├── restrictions.json    # Reglas y lógica de prohibiciones
│   └── ...
├── 📁 widgets/              # Módulos Lógicos
│   ├── buttons.py           # Navegación, transiciones y manejo de estado de UI
│   ├── checker.py           # Algoritmo de validación temporal y resolución de conflictos
│   ├── restrictions.py      # Motor de reglas de negocio
│   ├── hero_selector.py     # Lógica de interacción UI y suma global de atributos
│   └── ...
├── main.kv                  # Diseño de Interfaz (Kivy Language)
└── main.py                  # Ejecutable Principal

```

### 🚧 Dificultades Técnicas y Cómo se Resolvieron

1. **Manejo de Estados Compartidos:** Seleccionar un recurso en la interfaz altera la suma del equipo, el gráfico de radar, la disponibilidad y la validez de la misión. Coordinar esto fue complejo. **Solución:** Se centralizó el conteo de atributos globales en el contenedor principal, usando ese valor único como única fuente de verdad (Single Source of Truth) para actualizar el resto de widgets en cascada.
2. **Orden Cronológico e Integridad:** Guardar eventos de forma arbitraria dificultaba el *checker* temporal. **Solución:** Se implementó una subrutina que reordena y sanitiza automáticamente `events.json` tras cada inserción o borrado, garantizando que el algoritmo de disponibilidad trabaje sobre una línea temporal consistente.
3. **Estados Visuales Intermedios:** Transiciones o animaciones disparadas por el usuario a veces causaban colisiones lógicas si se pulsaban botones durante el proceso. **Solución:** Se implementaron bloqueos temporales de entrada (disable states) durante las animaciones para prevenir que el usuario rompa el flujo de estados.

---

## 🎓 Aprendizajes del Desarrollo y Mejoras Futuras

El desarrollo de este sistema me dejó aprendizajes fundamentales en ingeniería de software y diseño de interfaces:

* **Las interfaces son comunicación, no solo estética:** Los paneles, colores, y animaciones informan sobre la estructura y jerarquía de datos. El usuario entiende en todo momento qué le falta y qué seleccionó gracias a las confirmaciones visuales.
* **El valor de la Modularidad:** Un archivo monolítico habría sido inmanejable. Fragmentar la aplicación (`checker.py` para lógica, `chart.py` para gráficos, `date_selector.py` para inputs) redujo dramáticamente el tiempo de depuración y permitió reutilizar utilidades comunes (lectura/escritura JSON, búsqueda de nodos padres en Kivy).

**Posibles Mejoras Futuras:**
Aunque el proyecto cumple sus especificaciones, la escalabilidad de la arquitectura permite planear actualizaciones:

* **Edición en Caliente:** Implementar funcionalidad para editar eventos en curso (CRUD completo) en lugar de limitarlo a creación/eliminación.
* **Trazabilidad:** Un historial de auditoría para registrar *quién* y *cuándo* planificó cada despliegue.
* **Filtros de Búsqueda Avanzados:** En la vista de historial, añadir segmentación por recurso involucrado o nivel de éxito.

---

## 🚀 Guía de Instalación y Ejecución

Para desplegar el sistema en un entorno local, siga los siguientes pasos técnicos:

### 1. Clonación del Repositorio:

Asegúrese de disponer del código fuente en su máquina local.

### 2. Gestión de Dependencias:

El sistema requiere librerías específicas para su funcionamiento. Ejecute el siguiente comando para instalar los paquetes listados en `requirements.txt`:

```bash
pip install -r requirements.txt

```

### 3. Inicialización del Sistema:

Una vez configurado el entorno, ejecute el script principal para arrancar la aplicación:

```bash
python main.py

```

---

> *"Un gran poder conlleva una gran responsabilidad de gestión."*

<div align="center">

<br>
<br>
<br>
<br>
<br>
<br>

Por último, quiero quitarle las gracias a **Sergio**, por siempre estar ahí para darme los peores consejos de este framework. Sin él, seguramente habría terminado más rápido este proyecto.