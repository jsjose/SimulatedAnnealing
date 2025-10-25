# Visualización TSP - Simulated Annealing

## 🗺️ Nuevas Funcionalidades de Mapeo 2D

Se han añadido funciones de visualización para mostrar las ciudades y rutas del problema del Viajante de Comercio (TSP) en un mapa bidimensional.

### 📊 Funciones de Visualización Disponibles

#### 1. `mostrar_mapa_ciudades()`
- **Propósito**: Muestra todas las ciudades como puntos en un mapa 2D
- **Características**:
  - Puntos rojos para las ciudades
  - Etiquetas con nombres de ciudades (A, B, C, ...)
  - Grid de referencia
  - Coordenadas X e Y claramente marcadas

#### 2. `mostrar_ruta(ruta, titulo, color, mostrar_direccion)`
- **Propósito**: Visualiza una ruta específica conectando las ciudades
- **Parámetros**:
  - `ruta`: Lista de nombres de ciudades en orden
  - `titulo`: Título del gráfico
  - `color`: Color de las líneas y puntos
  - `mostrar_direccion`: Muestra flechas indicando dirección
- **Características**:
  - Líneas conectando las ciudades en orden
  - Circuito cerrado (regresa a la ciudad inicial)
  - Flechas direccionales opcionales
  - Cálculo y muestra del costo total

#### 3. `comparar_rutas(ruta_inicial, ruta_final)`
- **Propósito**: Comparación lado a lado de dos rutas
- **Características**:
  - Dos gráficos en una sola ventana
  - Ruta inicial en rojo vs ruta optimizada en verde
  - Costos mostrados para cada ruta
  - Misma escala para facilitar comparación

#### 4. `mostrar_info_ciudades()`
- **Propósito**: Información textual detallada del problema
- **Muestra**:
  - Coordenadas de todas las ciudades
  - Matriz parcial de distancias
  - Estadísticas del mapa (área, número de ciudades)

#### 5. `guardar_visualizaciones(ruta_inicial, ruta_final, prefijo_archivo)`
- **Propósito**: Guarda las visualizaciones como archivos PNG
- **Archivos generados**:
  - `{prefijo}_mapa_ciudades.png`: Mapa con todas las ciudades
  - `{prefijo}_comparacion.png`: Comparación de rutas inicial vs final
- **Calidad**: Alta resolución (300 DPI)

### 🚀 Flujo de Ejecución

1. **Inicialización**:
   - Genera ciudades aleatorias en un mapa 200x200
   - Muestra información detallada de las ciudades

2. **Visualización Inicial**:
   - Mapa de todas las ciudades
   - Ruta inicial (aleatoria) en rojo

3. **Optimización**:
   - Ejecuta Simulated Annealing
   - Muestra progreso cada 5000 iteraciones

4. **Resultados**:
   - Ruta optimizada en verde
   - Comparación lado a lado
   - Archivos PNG guardados localmente

### 📈 Información Mostrada

- **Coordenadas**: Posición (x, y) de cada ciudad
- **Distancias**: Cálculos euclidianos entre ciudades
- **Costos**: Distancia total de cada ruta
- **Mejora**: Porcentaje de optimización logrado
- **Progreso**: Temperatura y costos durante la optimización

### 🎨 Personalización Visual

- **Colores**: Rojo para inicial, verde para optimizada
- **Tamaños**: Puntos escalados para visibilidad
- **Etiquetas**: Nombres claros de ciudades
- **Flechas**: Dirección del recorrido
- **Grid**: Líneas de referencia

### 📋 Dependencias Requeridas

```python
import matplotlib.pyplot as plt
import numpy as np
```

Instalación:
```bash
pip install matplotlib numpy
```

### 🔧 Uso Práctico

El sistema es completamente automático. Al ejecutar `SimAnnealingTSP.py`:

1. Se generan ciudades aleatorias
2. Se muestran mapas interactivos
3. Se ejecuta la optimización
4. Se guardan resultados como imágenes

### 💡 Ventajas

- **Visual**: Comprensión intuitiva del problema y solución
- **Comparativo**: Fácil evaluación de la mejora
- **Documentado**: Archivos PNG para reportes
- **Educativo**: Ideal para enseñanza de algoritmos
- **Escalable**: Funciona con diferentes números de ciudades

### 🎯 Aplicaciones

- Educación en optimización
- Presentaciones de algoritmos
- Documentación de resultados
- Análisis de rendimiento
- Debugging visual de rutas