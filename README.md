# 🚀 Quantum TSP Optimizer - Comparación de Formulaciones Clásica vs QUBO

Un framework modular de optimización que implementa y compara diferentes formulaciones del Problema del Viajante de Comercio (TSP) utilizando el algoritmo Simulated Annealing.

## 📋 Descripción del Proyecto

Este proyecto implementa una arquitectura modular que permite comparar el rendimiento de diferentes formulaciones matemáticas del TSP:

- **Formulación Clásica**: Representación tradicional usando permutaciones de ciudades
- **Formulación QUBO**: Formulación cuadrática binaria compatible con computación cuántica

## 🏗️ Arquitectura del Sistema

```
📁 quantum/
├── 🧮 simulated_annealing.py          # Algoritmo genérico de SA
├── 🏙️  tsp_base.py                    # Utilidades comunes del TSP  
├── 🔄 tsp_classical.py                # Formulación clásica
├── ⚛️  tsp_qubo.py                     # Formulación QUBO
├── ⚖️  compare_formulations.py        # Comparador de formulaciones
├── 🧪 ejemplo_comparacion.py          # Ejemplos de uso
└── 📚 README.md                       # Este archivo
```

### Módulos Principales

#### 🧮 `simulated_annealing.py`
**Algoritmo genérico de Simulated Annealing**
- Clase abstracta `OptimizationProblem` para definir interfaces de problemas
- Implementación genérica de SA que funciona con cualquier problema
- Estadísticas de convergencia y visualización de progreso
- Soporte para múltiples ejecuciones con análisis estadístico

#### 🏙️ `tsp_base.py`
**Utilidades comunes para formulaciones TSP**
- **Generación de ciudades**: Uniformes, clusters, aleatorias
- **Visualización**: Mapas 2D, rutas, comparaciones
- **Cálculos**: Distancias euclídeas, costos de tours
- **Validación**: Verificación de soluciones válidas

#### 🔄 `tsp_classical.py`
**Formulación tradicional del TSP**
- Representación por permutaciones de ciudades
- Operadores de vecindario: 2-opt, swap, reverse, insert
- Optimización local para mejorar soluciones
- Compatible con el framework genérico de SA

#### ⚛️ `tsp_qubo.py`
**Formulación QUBO (Quadratic Unconstrained Binary Optimization)**
- Representación matricial binaria (n×n)
- Construcción automática de matriz Q con penalizaciones
- Restricciones: Cada ciudad visitada exactamente una vez
- Conversión entre representación binaria y rutas
- **Compatible con computación cuántica**

#### ⚖️ `compare_formulations.py`
**Sistema de comparación entre formulaciones**
- Análisis comparativo de rendimiento
- Métricas: tiempo de ejecución, calidad de soluciones, validez
- Visualizaciones: gráficos de progreso, estadísticas, comparación de rutas
- Análisis estadístico con múltiples ejecuciones

## 🚀 Uso Rápido

### Instalación de Dependencias
```bash
pip install matplotlib numpy
```

### Ejemplo Básico
```python
from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

# Generar ciudades
ciudades = tsp.generar_ciudades_uniformes(8, 200)

# Crear comparador
comparador = TSPFormulationComparator(ciudades)

# Parámetros de Simulated Annealing
sa_params = {
    'initial_temperature': 1000.0,
    'final_temperature': 0.1,
    'cooling_rate': 0.99
}

# Ejecutar comparación
resultado = comparador.compare_single_run(sa_params)

# Visualizar resultados
comparador.visualize_comparison(resultado)
```

### Ejecutar Ejemplos Completos
```bash
# Ejemplo interactivo con múltiples opciones
python ejemplo_comparacion.py

# Comparación completa desde el script principal
python compare_formulations.py
```

## 📊 Tipos de Análisis Disponibles

### 1. Comparación Individual
Ejecuta ambas formulaciones en el mismo problema y compara:
- ⏱️ Tiempo de ejecución
- 💰 Costo final del tour
- ✅ Validez de soluciones (especialmente para QUBO)
- 📈 Progreso de convergencia

### 2. Análisis Estadístico
Múltiples ejecuciones independientes para obtener:
- 📊 Distribuciones de costos y tiempos
- 🏆 Tasa de victoria por formulación
- 📈 Estadísticas de validez de QUBO
- 🎯 Confiabilidad de cada enfoque

### 3. Análisis de Escalabilidad
Evaluación del rendimiento con diferentes tamaños de problema:
- 📈 Cómo escala el tiempo de ejecución
- 🎯 Límites prácticos de cada formulación
- ⚖️ Trade-offs entre complejidad y calidad

## 🎨 Topologías de Ciudades

El sistema soporta múltiples tipos de distribución de ciudades:

```python
# Ciudades distribuidas uniformemente
ciudades_uniformes = tsp.generar_ciudades_uniformes(n=10, mapa_size=200)

# Ciudades agrupadas en clusters
ciudades_clusters = tsp.generar_ciudades_clusters(n=12, mapa_size=200, num_clusters=3)

# Ciudades con distribución aleatoria
ciudades_aleatorias = tsp.generar_ciudades_aleatorias(n=8, mapa_size=150)
```

## ⚛️ Formulación QUBO Explicada

### Representación Matemática

La formulación QUBO convierte el TSP en un problema de optimización cuadrática:

```
Minimizar: x^T * Q * x

Donde:
- x es un vector binario de n² variables
- Q es la matriz QUBO que incluye costos y penalizaciones
- x[i,j] = 1 si la ciudad i es visitada en la posición j
```

### Restricciones como Penalizaciones

```python
# Restricción 1: Cada ciudad visitada exactamente una vez
# Penalización: P₁ * (Σⱼ x[i,j] - 1)²

# Restricción 2: Cada posición ocupada por exactamente una ciudad  
# Penalización: P₂ * (Σᵢ x[i,j] - 1)²
```

### Ventajas de QUBO

- 🔮 **Compatibilidad cuántica**: Ejecutable en computadoras cuánticas
- 🧮 **Formulación estándar**: Permite usar optimizadores QUBO especializados
- 🔄 **Flexibilidad**: Fácil agregar nuevas restricciones como penalizaciones

### Desafíos de QUBO

- 📈 **Complejidad**: O(n⁴) en espacio y tiempo vs O(n²) clásico
- ⚖️ **Penalizaciones**: Requiere ajuste cuidadoso de factores de penalización
- 🎯 **Validación**: Soluciones pueden violar restricciones si penalizaciones son insuficientes

## 📈 Interpretación de Resultados

### Métricas Clave

```
=== RESUMEN COMPARATIVO ===
Costo tour clásico: 245.67
Costo tour QUBO: 251.23
Diferencia de costo: 5.56
Ratio de costo (QUBO/Clásico): 1.023
Ratio de tiempo (QUBO/Clásico): 3.45
Mejor formulación: CLÁSICO
QUBO válido: True
```

**Interpretación**:
- **Costo tour**: Métrica principal - distancia total del recorrido
- **Ratio de costo**: QUBO vs Clásico (1.0 = igual, >1.0 = QUBO peor)
- **Ratio de tiempo**: Cuánto más lento es QUBO
- **QUBO válido**: Si la solución respeta las restricciones del TSP

### Cuándo Usar Cada Formulación

#### 🔄 Formulación Clásica
- ✅ **Úsala cuando**: Necesites rapidez y eficiencia
- ✅ **Ventajas**: Rápida, menos memoria, siempre válida
- ❌ **Limitaciones**: Solo para computación clásica

#### ⚛️ Formulación QUBO  
- ✅ **Úsala cuando**: Planees usar computación cuántica o híbrida
- ✅ **Ventajas**: Compatible con quantum annealers, formato estándar
- ❌ **Limitaciones**: Más lenta, requiere más memoria, soluciones ocasionalmente inválidas

## 🔧 Configuración Avanzada

### Parámetros de Simulated Annealing

```python
sa_params = {
    'initial_temperature': 1000.0,    # Temperatura inicial (mayor = más exploración)
    'final_temperature': 0.1,         # Temperatura final (menor = más explotación)  
    'cooling_rate': 0.99,             # Factor de enfriamiento (0.9-0.99 típico)
    'verbose': True,                  # Mostrar progreso detallado
    'progress_interval': 1000         # Frecuencia de reporte de progreso
}
```

### Operadores de Vecindario (Clásico)

```python
# Diferentes operadores disponibles
tsp_2opt = TSPClassical(ciudades, operacion_vecindario="2opt")      # Intercambio de arcos
tsp_swap = TSPClassical(ciudades, operacion_vecindario="swap")      # Intercambio de ciudades
tsp_reverse = TSPClassical(ciudades, operacion_vecindario="reverse") # Inversión de segmentos
tsp_insert = TSPClassical(ciudades, operacion_vecindario="insert")   # Reinserción de ciudades
```

### Factor de Penalización (QUBO)

```python
# Ajustar factor de penalización para QUBO
tsp_qubo_suave = TSPQUBO(ciudades, penalty_factor=500.0)   # Penalización suave
tsp_qubo_fuerte = TSPQUBO(ciudades, penalty_factor=2000.0) # Penalización fuerte
```

## 🧪 Ejemplos de Casos de Uso

### Caso 1: Investigación Académica
```python
# Comparación rigurosa con múltiples métricas
estadisticas = comparador.compare_multiple_runs(sa_params, num_runs=10)
comparador.visualize_statistics(estadisticas)
```

### Caso 2: Prototipado Rápido
```python
# Prueba rápida de concepto
from ejemplo_comparacion import ejemplo_comparacion_rapida
resultado = ejemplo_comparacion_rapida()
```

### Caso 3: Análisis de Rendimiento
```python  
# Evaluar escalabilidad
from ejemplo_comparacion import ejemplo_analisis_escalabilidad
resultados = ejemplo_analisis_escalabilidad()
```

## 🤝 Extensibilidad

### Agregar Nueva Formulación

```python
from simulated_annealing import OptimizationProblem

class TSPNuevaFormulacion(OptimizationProblem):
    def generate_initial_solution(self):
        # Tu implementación aquí
        pass
    
    def get_neighbor(self, solution):
        # Tu implementación aquí  
        pass
    
    def calculate_cost(self, solution):
        # Tu implementación aquí
        pass
    
    def is_valid_solution(self, solution):
        # Tu implementación aquí
        pass
```

### Agregar Nuevo Problema de Optimización

El framework es genérico y puede manejar cualquier problema que implemente `OptimizationProblem`:

```python
class ProblemaPersonalizado(OptimizationProblem):
    # Implementar métodos requeridos
    pass

# Usar con Simulated Annealing
sa = SimulatedAnnealing(ProblemaPersonalizado(), **params)
solution, cost, stats = sa.optimize()
```

## 📚 Dependencias

- **Python 3.8+**
- **matplotlib**: Visualización de gráficos y mapas
- **numpy**: Operaciones matriciales y cálculos numéricos

## 🐛 Troubleshooting

### Problema: QUBO produce soluciones inválidas
**Solución**: Incrementar `penalty_factor` en `TSPQUBO`

### Problema: SA converge muy rápido
**Solución**: Usar `cooling_rate` más cercano a 1.0 (ej: 0.995)

### Problema: Tiempo de ejecución muy lento
**Solución**: Reducir `initial_temperature` o usar `cooling_rate` más agresivo (ej: 0.9)

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

🎉 **¡Disfruta explorando las diferencias entre optimización clásica y cuántica con el TSP!** 🎉