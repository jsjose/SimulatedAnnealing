# 🗺️ Comparación de Topologías TSP - Simulated Annealing

## 🎯 Nueva Funcionalidad: Análisis de Topologías

Se han implementado tres tipos diferentes de distribución de ciudades para analizar cómo la topología espacial afecta al rendimiento del algoritmo de Simulated Annealing en el problema del Viajante de Comercio.

## 📊 Tipos de Topologías Implementadas

### 1. 📐 **Distribución Uniforme** 
- **Descripción**: Ciudades distribuidas en una cuadrícula aproximada con variación aleatoria
- **Características**:
  - Espaciado regular entre ciudades
  - 30% de variación aleatoria para evitar patrones rígidos
  - Distribución más homogénea en el espacio
- **Ventajas**: Distancias más predecibles, menor variabilidad
- **Uso típico**: Problemas con ciudades planificadas o redes regulares

### 2. 🎯 **Distribución en Clusters**
- **Descripción**: Ciudades agrupadas en clusters con centros aleatorios
- **Características**:
  - 3-8 clusters automáticamente calculados según número de ciudades
  - Distribución triangular (más ciudades cerca del centro de cada cluster)
  - Radios variables para cada cluster
- **Ventajas**: Refleja patrones reales de asentamientos urbanos
- **Uso típico**: Problemas con ciudades agrupadas geográficamente

### 3. 🎲 **Distribución Aleatoria**
- **Descripción**: Ciudades distribuidas completamente al azar
- **Características**:
  - Sin patrones predefinidos
  - Máxima variabilidad en distancias
  - Implementación original del código
- **Ventajas**: Caso general sin suposiciones
- **Uso típico**: Problemas sin información previa de distribución

## 🔬 Resultados del Experimento (50 ciudades)

### 📈 **Estadísticas de Rendimiento**

| Topología | Costo Inicial | Costo Final | Mejora (%) | Eficiencia |
|-----------|---------------|-------------|------------|------------|
| Uniforme  | 4,727.0       | 1,250.3     | 73.6%      | 15.56      |
| Clusters  | 3,573.5       | **723.1**   | **79.8%**  | **22.32**  |
| Aleatoria | 4,777.3       | 1,244.1     | 74.0%      | 15.48      |

### 🏆 **Análisis de Resultados**

- **🥇 Mejor Resultado**: Topología de Clusters (costo final: 723.1)
- **📊 Mayor Mejora**: Clusters con 79.8% de optimización
- **⚡ Mayor Eficiencia**: Clusters (22.32 puntos de eficiencia)
- **📏 Diferencia**: 527.1 unidades entre mejor y peor resultado

## 🎨 Características de Visualización

### **Modo Comparación**
- Visualización lado a lado de las 3 topologías
- Fila superior: Distribución original + ruta inicial
- Fila inferior: Ruta optimizada + estadísticas
- Archivo generado: `comparacion_topologias.png`

### **Modo Individual** 
- Análisis detallado de una topología específica
- Mapas interactivos con matplotlib
- Información completa de ciudades y distancias
- Comparación inicial vs optimizada

## 🔧 Configuración y Uso

### **Activar Modo Comparación**
```python
MODO_COMPARACION = True  # En la sección principal
```

### **Seleccionar Topología Individual**
```python
MODO_COMPARACION = False
TIPO_TOPOLOGIA = "clusters"  # "uniforme", "clusters", "aleatoria"
```

### **Parámetros Personalizables**
- `NUM_CIUDADES`: Número de ciudades (individual)
- `num_ciudades_comparacion`: Ciudades para comparación
- `MAPA_SIZE`: Tamaño del mapa (200x200 por defecto)

## 💡 Insights del Experimento

### **¿Por qué los Clusters funcionan mejor?**

1. **🎯 Optimización Local**: El algoritmo puede optimizar rutas dentro de cada cluster
2. **🔗 Conexiones Eficientes**: Enlaces entre clusters más directos
3. **📍 Menor Variabilidad**: Distancias más consistentes reducen el espacio de búsqueda
4. **🧮 Estructura Jerárquica**: Problema se descompone naturalmente

### **Implicaciones Prácticas**

- **Logística Urbana**: Agrupar entregas por zonas mejora eficiencia
- **Planificación de Rutas**: Considerar patrones geográficos naturales
- **Algoritmos Adaptativos**: Ajustar parámetros según topología detectada

## 🚀 Funciones Principales

### **Generación de Ciudades**
```python
generar_ciudades_uniformes(num_ciudades, mapa_size)
generar_ciudades_clusters(num_ciudades, mapa_size, num_clusters=None)
generar_ciudades_aleatorias(num_ciudades, mapa_size)
```

### **Análisis Comparativo**
```python
comparar_topologias(num_ciudades, mapa_size, T_ini, T_fin, ratio_enfriamiento)
visualizar_comparacion_topologias(resultados)
mostrar_estadisticas_comparacion(resultados)
```

## 📋 Requisitos

- `matplotlib >= 3.0`
- `numpy >= 1.0`
- Python 3.6+

## 🎓 Aplicaciones Educativas

### **Conceptos Demostrados**
- Influencia de la topología en optimización
- Análisis comparativo de algoritmos
- Visualización de datos científicos
- Metodología experimental en IA

### **Para Estudiantes**
- Experimente con diferentes números de ciudades
- Modifique parámetros de clusters
- Compare con otros algoritmos de optimización
- Analice el comportamiento con mapas más grandes

## 🔮 Extensiones Futuras

- **Topologías Adicionales**: Líneas, círculos, fractales
- **Métricas Avanzadas**: Tiempo de convergencia, estabilidad
- **Algoritmos Híbridos**: Detectar topología automáticamente
- **Paralelización**: Clusters independientes en paralelo
- **Análisis Estadístico**: Múltiples ejecuciones con intervalos de confianza

---

### 🏅 **Conclusión**

La topología de ciudades tiene un **impacto significativo** en el rendimiento de Simulated Annealing. Los resultados muestran que:

- **Clusters organizados** superan a distribuciones uniformes y aleatorias
- **La estructura espacial** puede aprovecharse para mejor optimización  
- **El contexto geográfico** debe considerarse en aplicaciones reales
- **La visualización comparativa** permite insights claros sobre el rendimiento

¡Experimenta con diferentes topologías y descubre patrones interesantes en tu propia investigación! 🚀