"""
Librería base para problemas del Traveling Salesman Problem (TSP)

Contiene funciones comunes para diferentes formulaciones del TSP:
- Generación de ciudades (uniforme, clusters, aleatoria)
- Cálculo de distancias
- Visualización
- Análisis de resultados

Autor: Sistema de Optimización Cuántica
Fecha: Octubre 2025
"""

import random
import math
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import numpy as np


def generar_nombre_ciudad(indice: int) -> str:
    """
    Genera nombres de ciudades usando combinaciones de dos letras.
    Ej: 0->AA, 1->AB, 2->AC, ..., 25->AZ, 26->BA, 27->BB, etc.
    
    Args:
        indice: Índice numérico de la ciudad (0, 1, 2, ...)
        
    Returns:
        Nombre de la ciudad (AA, AB, AC, ...)
    """
    primera_letra = chr(65 + (indice // 26))  # A, B, C, ...
    segunda_letra = chr(65 + (indice % 26))   # A-Z para cada primera letra
    return primera_letra + segunda_letra


def calcular_distancia_euclidiana(coord1: Tuple[float, float], 
                                 coord2: Tuple[float, float]) -> float:
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        coord1: Coordenadas (x, y) del primer punto
        coord2: Coordenadas (x, y) del segundo punto
        
    Returns:
        Distancia euclidiana entre los puntos
    """
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])


def generar_ciudades_uniformes(num_ciudades: int, mapa_size: int) -> Dict[str, Tuple[int, int]]:
    """
    Genera ciudades distribuidas uniformemente en el mapa.
    Utiliza una cuadrícula aproximada para distribución más uniforme.
    
    Args:
        num_ciudades: Número de ciudades a generar
        mapa_size: Tamaño del mapa (cuadrado)
        
    Returns:
        Diccionario {nombre_ciudad: (x, y)}
    """
    ciudades = {}
    
    # Calcular dimensiones de la cuadrícula más cercana
    lado_cuadricula = int(math.ceil(math.sqrt(num_ciudades)))
    espaciado_x = mapa_size / lado_cuadricula
    espaciado_y = mapa_size / lado_cuadricula
    
    # Agregar un poco de aleatoriedad para evitar patrones demasiado rígidos
    variacion = min(espaciado_x, espaciado_y) * 0.3  # 30% de variación
    
    for i in range(num_ciudades):
        nombre = generar_nombre_ciudad(i)
        
        # Posición en la cuadrícula
        fila = i // lado_cuadricula
        columna = i % lado_cuadricula
        
        # Coordenadas base de la cuadrícula
        x_base = columna * espaciado_x + espaciado_x / 2
        y_base = fila * espaciado_y + espaciado_y / 2
        
        # Agregar variación aleatoria
        x = max(0, min(mapa_size, x_base + random.uniform(-variacion, variacion)))
        y = max(0, min(mapa_size, y_base + random.uniform(-variacion, variacion)))
        
        ciudades[nombre] = (int(x), int(y))
    
    return ciudades


def generar_ciudades_clusters(num_ciudades: int, mapa_size: int, 
                             num_clusters: Optional[int] = None) -> Dict[str, Tuple[int, int]]:
    """
    Genera ciudades agrupadas en clusters.
    
    Args:
        num_ciudades: Número total de ciudades
        mapa_size: Tamaño del mapa
        num_clusters: Número de clusters (si es None, se calcula automáticamente)
        
    Returns:
        Diccionario {nombre_ciudad: (x, y)}
    """
    ciudades = {}
    
    # Calcular número de clusters automáticamente si no se especifica
    if num_clusters is None:
        num_clusters = max(3, min(8, int(math.sqrt(num_ciudades / 10))))  # Entre 3 y 8 clusters
    
    # Generar centros de clusters aleatorios
    margen = mapa_size * 0.15  # 15% de margen desde los bordes
    centros_clusters = []
    for _ in range(num_clusters):
        centro_x = random.uniform(margen, mapa_size - margen)
        centro_y = random.uniform(margen, mapa_size - margen)
        centros_clusters.append((centro_x, centro_y))
    
    # Radio base para cada cluster
    radio_base = mapa_size / (2 * math.sqrt(num_clusters))
    
    # Asignar ciudades a clusters
    ciudades_por_cluster = num_ciudades // num_clusters
    ciudades_extras = num_ciudades % num_clusters
    
    indice_ciudad = 0
    for i, (centro_x, centro_y) in enumerate(centros_clusters):
        # Algunas clusters tendrán una ciudad extra
        num_en_este_cluster = ciudades_por_cluster + (1 if i < ciudades_extras else 0)
        
        # Radio específico para este cluster (con variación)
        radio_cluster = radio_base * random.uniform(0.7, 1.3)
        
        for _ in range(num_en_este_cluster):
            nombre = generar_nombre_ciudad(indice_ciudad)
            
            # Generar posición dentro del cluster usando distribución normal
            angulo = random.uniform(0, 2 * math.pi)
            # Usar distribución que concentra más ciudades cerca del centro
            distancia = random.triangular(0, radio_cluster, radio_cluster * 0.3)
            
            x = centro_x + distancia * math.cos(angulo)
            y = centro_y + distancia * math.sin(angulo)
            
            # Asegurar que la ciudad esté dentro del mapa
            x = max(0, min(mapa_size, x))
            y = max(0, min(mapa_size, y))
            
            ciudades[nombre] = (int(x), int(y))
            indice_ciudad += 1
    
    return ciudades


def generar_ciudades_aleatorias(num_ciudades: int, mapa_size: int) -> Dict[str, Tuple[int, int]]:
    """
    Genera ciudades completamente aleatorias.
    
    Args:
        num_ciudades: Número de ciudades
        mapa_size: Tamaño del mapa
        
    Returns:
        Diccionario {nombre_ciudad: (x, y)}
    """
    ciudades = {}
    for i in range(num_ciudades):
        nombre = generar_nombre_ciudad(i)
        ciudades[nombre] = (random.randint(0, mapa_size), random.randint(0, mapa_size))
    return ciudades


def calcular_matriz_distancias(ciudades: Dict[str, Tuple[int, int]]) -> Dict[Tuple[str, str], float]:
    """
    Calcula la matriz de distancias entre todas las ciudades.
    
    Args:
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        
    Returns:
        Diccionario {(ciudad1, ciudad2): distancia}
    """
    matriz_distancias = {}
    nombres = list(ciudades.keys())
    
    for i, ciudad1 in enumerate(nombres):
        for j, ciudad2 in enumerate(nombres[i:], i):
            if i == j:
                distancia = 0.0
            else:
                distancia = calcular_distancia_euclidiana(ciudades[ciudad1], ciudades[ciudad2])
            
            matriz_distancias[(ciudad1, ciudad2)] = distancia
            matriz_distancias[(ciudad2, ciudad1)] = distancia
    
    return matriz_distancias


def calcular_costo_ruta(ruta: List[str], ciudades: Dict[str, Tuple[int, int]]) -> float:
    """
    Calcula el costo total de una ruta (distancia total).
    
    Args:
        ruta: Lista de nombres de ciudades en orden
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        
    Returns:
        Costo total de la ruta
    """
    if len(ruta) < 2:
        return 0.0
    
    costo_total = 0.0
    num_ciudades = len(ruta)
    
    for i in range(num_ciudades):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % num_ciudades]  # Circuito cerrado
        costo_total += calcular_distancia_euclidiana(ciudades[ciudad_actual], 
                                                    ciudades[ciudad_siguiente])
    
    return costo_total


def mostrar_mapa_ciudades(ciudades: Dict[str, Tuple[int, int]], 
                         titulo: str = "Mapa de Ciudades",
                         mapa_size: int = 200,
                         mostrar_nombres: bool = True,
                         tamaño_figura: Tuple[int, int] = (10, 8)):
    """
    Muestra un mapa con todas las ciudades y sus coordenadas.
    
    Args:
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        titulo: Título del gráfico
        mapa_size: Tamaño del mapa para los límites
        mostrar_nombres: Si mostrar nombres de ciudades
        tamaño_figura: Tamaño de la figura (ancho, alto)
    """
    plt.figure(figsize=tamaño_figura)
    
    # Extraer coordenadas
    x_coords = [coord[0] for coord in ciudades.values()]
    y_coords = [coord[1] for coord in ciudades.values()]
    
    # Dibujar ciudades como puntos
    plt.scatter(x_coords, y_coords, c='red', s=100, alpha=0.7)
    
    # Añadir etiquetas con los nombres de las ciudades
    if mostrar_nombres and len(ciudades) <= 50:  # Solo si no hay demasiadas ciudades
        for nombre, (x, y) in ciudades.items():
            plt.annotate(nombre, (x, y), xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, fontweight='bold')
    
    plt.title(titulo, fontsize=14)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-10, mapa_size + 10)
    plt.ylim(-10, mapa_size + 10)
    plt.show()


def mostrar_ruta(ruta: List[str], 
                ciudades: Dict[str, Tuple[int, int]], 
                titulo: str = "Ruta TSP", 
                color: str = 'blue',
                mapa_size: int = 200,
                mostrar_direccion: bool = True,
                mostrar_nombres: bool = False,
                tamaño_figura: Tuple[int, int] = (12, 8)):
    """
    Muestra un mapa con la ruta especificada.
    
    Args:
        ruta: Lista de nombres de ciudades en orden
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        titulo: Título del gráfico
        color: Color de las líneas de la ruta
        mapa_size: Tamaño del mapa para los límites
        mostrar_direccion: Si mostrar flechas indicando la dirección
        mostrar_nombres: Si mostrar nombres de ciudades
        tamaño_figura: Tamaño de la figura
    """
    plt.figure(figsize=tamaño_figura)
    
    # Extraer coordenadas de todas las ciudades
    x_coords = [coord[0] for coord in ciudades.values()]
    y_coords = [coord[1] for coord in ciudades.values()]
    
    # Dibujar todas las ciudades como puntos grises
    plt.scatter(x_coords, y_coords, c='lightgray', s=80, alpha=0.5, zorder=1)
    
    # Extraer coordenadas de la ruta
    ruta_x = [ciudades[ciudad][0] for ciudad in ruta]
    ruta_y = [ciudades[ciudad][1] for ciudad in ruta]
    
    # Cerrar el circuito (volver al punto inicial)
    ruta_x.append(ruta_x[0])
    ruta_y.append(ruta_y[0])
    
    # Dibujar la ruta
    plt.plot(ruta_x, ruta_y, color=color, linewidth=2, alpha=0.8, zorder=2)
    
    # Dibujar las ciudades de la ruta como puntos destacados
    plt.scatter(ruta_x[:-1], ruta_y[:-1], c=color, s=120, alpha=0.9, zorder=3)
    
    # Añadir nombres de ciudades si se solicita
    if mostrar_nombres and len(ciudades) <= 30:
        for nombre, (x, y) in ciudades.items():
            plt.annotate(nombre, (x, y), xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, fontweight='bold')
    
    # Añadir flechas para mostrar la dirección si se solicita
    if mostrar_direccion and len(ruta) <= 30:  # Solo para rutas pequeñas
        for i in range(len(ruta)):
            x1, y1 = ciudades[ruta[i]]
            x2, y2 = ciudades[ruta[(i + 1) % len(ruta)]]
            
            # Calcular punto medio para colocar la flecha
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Calcular dirección
            dx = x2 - x1
            dy = y2 - y1
            
            # Dibujar flecha pequeña en el punto medio
            plt.annotate('', xy=(mid_x + dx*0.1, mid_y + dy*0.1), 
                        xytext=(mid_x - dx*0.1, mid_y - dy*0.1),
                        arrowprops={'arrowstyle': '->', 'color': color, 'lw': 1.5})
    
    # Calcular y mostrar el costo de la ruta
    costo = calcular_costo_ruta(ruta, ciudades)
    plt.title(f'{titulo} - Costo: {costo:.2f}', fontsize=14)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-10, mapa_size + 10)
    plt.ylim(-10, mapa_size + 10)
    plt.show()


def comparar_rutas(ruta1: List[str], ruta2: List[str], 
                  ciudades: Dict[str, Tuple[int, int]],
                  etiquetas: Tuple[str, str] = ("Ruta 1", "Ruta 2"),
                  colores: Tuple[str, str] = ('red', 'green'),
                  mapa_size: int = 200,
                  tamaño_figura: Tuple[int, int] = (16, 8)):
    """
    Muestra una comparación lado a lado de dos rutas.
    
    Args:
        ruta1: Primera ruta a comparar
        ruta2: Segunda ruta a comparar
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        etiquetas: Etiquetas para las rutas
        colores: Colores para las rutas
        mapa_size: Tamaño del mapa
        tamaño_figura: Tamaño de la figura
    """
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=tamaño_figura)
    
    # Función auxiliar para dibujar una ruta en un subplot específico
    def dibujar_en_subplot(ax, ruta, titulo, color):
        # Todas las ciudades en gris
        x_coords = [coord[0] for coord in ciudades.values()]
        y_coords = [coord[1] for coord in ciudades.values()]
        ax.scatter(x_coords, y_coords, c='lightgray', s=80, alpha=0.5)
        
        # Ruta específica
        ruta_x = [ciudades[ciudad][0] for ciudad in ruta]
        ruta_y = [ciudades[ciudad][1] for ciudad in ruta]
        ruta_x.append(ruta_x[0])  # Cerrar circuito
        ruta_y.append(ruta_y[0])
        
        ax.plot(ruta_x, ruta_y, color=color, linewidth=2, alpha=0.8)
        ax.scatter(ruta_x[:-1], ruta_y[:-1], c=color, s=120, alpha=0.9)
        
        # Nombres solo para pocas ciudades
        if len(ciudades) <= 20:
            for nombre, (x, y) in ciudades.items():
                ax.annotate(nombre, (x, y), xytext=(3, 3), textcoords='offset points', 
                           fontsize=8, fontweight='bold')
        
        costo = calcular_costo_ruta(ruta, ciudades)
        ax.set_title(f'{titulo} - Costo: {costo:.2f}', fontsize=12)
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, mapa_size + 10)
        ax.set_ylim(-10, mapa_size + 10)
    
    # Dibujar ambas rutas
    dibujar_en_subplot(ax1, ruta1, etiquetas[0], colores[0])
    dibujar_en_subplot(ax2, ruta2, etiquetas[1], colores[1])
    
    plt.tight_layout()
    plt.show()


def mostrar_info_ciudades(ciudades: Dict[str, Tuple[int, int]], mapa_size: int = 200):
    """
    Muestra información detallada de todas las ciudades y sus distancias.
    
    Args:
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        mapa_size: Tamaño del mapa
    """
    print("\n=== INFORMACIÓN DETALLADA DE CIUDADES ===")
    print(f"Total de ciudades: {len(ciudades)}")
    print(f"Área del mapa: {mapa_size} x {mapa_size}")
    print("\nCoordenadas de las ciudades:")
    
    for nombre, (x, y) in sorted(ciudades.items()):
        print(f"  {nombre}: ({x:3d}, {y:3d})")
    
    # Mostrar matriz de distancias parcial
    nombres_muestra = sorted(ciudades.keys())[:6]  # Primeras 6 ciudades
    if len(nombres_muestra) > 1:
        print("\nMatriz de distancias (muestra parcial):")
        print("     ", end="")
        for nombre in nombres_muestra:
            print(f"{nombre:9s}", end="")
        print()
        
        for i, ciudad1 in enumerate(nombres_muestra):
            print(f"{ciudad1:4s} ", end="")
            for j, ciudad2 in enumerate(nombres_muestra):
                if i <= j:
                    distancia = calcular_distancia_euclidiana(ciudades[ciudad1], ciudades[ciudad2])
                    print(f"{distancia:8.1f} ", end="")
                else:
                    print(f"{'':9s}", end="")
            print()
        
        if len(ciudades) > 6:
            print("  ... (matriz completa omitida para claridad)")
    
    print("="*50)


def validar_ruta(ruta: List[str], ciudades: Dict[str, Tuple[int, int]]) -> bool:
    """
    Valida que una ruta sea válida para el TSP.
    
    Args:
        ruta: Lista de nombres de ciudades
        ciudades: Diccionario de ciudades disponibles
        
    Returns:
        True si la ruta es válida
    """
    # Verificar que todas las ciudades en la ruta existen
    for ciudad in ruta:
        if ciudad not in ciudades:
            return False
    
    # Verificar que no haya ciudades duplicadas
    if len(set(ruta)) != len(ruta):
        return False
    
    # Verificar que incluya todas las ciudades
    if set(ruta) != set(ciudades.keys()):
        return False
    
    return True


def generar_ruta_aleatoria(ciudades: Dict[str, Tuple[int, int]]) -> List[str]:
    """
    Genera una ruta aleatoria válida que visite todas las ciudades.
    
    Args:
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        
    Returns:
        Lista de nombres de ciudades en orden aleatorio
    """
    nombres = list(ciudades.keys())
    random.shuffle(nombres)
    return nombres


def generar_ruta_greedy_nearest_neighbor(ciudades: Dict[str, Tuple[int, int]], 
                                       ciudad_inicio: Optional[str] = None) -> List[str]:
    """
    Genera una ruta usando el algoritmo greedy del vecino más cercano.
    
    Args:
        ciudades: Diccionario {nombre_ciudad: (x, y)}
        ciudad_inicio: Ciudad de inicio (None para aleatoria)
        
    Returns:
        Lista de nombres de ciudades usando nearest neighbor
    """
    nombres = list(ciudades.keys())
    if not nombres:
        return []
    
    if ciudad_inicio is None:
        ciudad_inicio = random.choice(nombres)
    
    ruta = [ciudad_inicio]
    ciudades_restantes = set(nombres) - {ciudad_inicio}
    
    while ciudades_restantes:
        ciudad_actual = ruta[-1]
        ciudad_mas_cercana = min(ciudades_restantes, 
                                key=lambda c: calcular_distancia_euclidiana(
                                    ciudades[ciudad_actual], ciudades[c]))
        ruta.append(ciudad_mas_cercana)
        ciudades_restantes.remove(ciudad_mas_cercana)
    
    return ruta