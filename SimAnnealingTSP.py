import random
import math
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Definición del Problema (TSP) ---

# A. Datos del problema (Generamos N ciudades aleatorias en un mapa 2D)
NUM_CIUDADES = 150
MAPA_SIZE = 200

def generar_nombre_ciudad(indice):
    """
    Genera nombres de ciudades usando combinaciones de dos letras.
    Ej: 0->AA, 1->AB, 2->AC, ..., 25->AZ, 26->BA, 27->BB, etc.
    """
    primera_letra = chr(65 + (indice // 26))  # A, B, C, ...
    segunda_letra = chr(65 + (indice % 26))   # A-Z para cada primera letra
    return primera_letra + segunda_letra

def generar_ciudades_uniformes(num_ciudades, mapa_size):
    """
    Genera ciudades distribuidas uniformemente en el mapa.
    Utiliza una cuadrícula aproximada para distribución más uniforme.
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

def generar_ciudades_clusters(num_ciudades, mapa_size, num_clusters=None):
    """
    Genera ciudades agrupadas en clusters.
    
    Args:
        num_ciudades: Número total de ciudades
        mapa_size: Tamaño del mapa
        num_clusters: Número de clusters (si es None, se calcula automáticamente)
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
        
        for j in range(num_en_este_cluster):
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

def generar_ciudades_aleatorias(num_ciudades, mapa_size):
    """
    Genera ciudades completamente aleatorias (implementación original).
    """
    ciudades = {}
    for i in range(num_ciudades):
        nombre = generar_nombre_ciudad(i)
        ciudades[nombre] = (random.randint(0, mapa_size), random.randint(0, mapa_size))
    return ciudades

# Generar ciudades por defecto (se modificará en la función principal)
ciudades = generar_ciudades_aleatorias(NUM_CIUDADES, MAPA_SIZE)

lista_ciudades = list(ciudades.keys())

# B. Función de ayuda para calcular la distancia euclidiana
def dist(c1_nombre, c2_nombre):
    """Calcula la distancia entre dos ciudades por su nombre."""
    coord1 = ciudades[c1_nombre]
    coord2 = ciudades[c2_nombre]
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])

# --- C. Funciones requeridas por SA ---

def calcular_costo(ruta):
    """
    Calcula el costo (distancia total) de una ruta.
    'ruta' es una lista de nombres de ciudades, ej: ['A', 'C', 'B', ...]
    """
    costo_total = 0
    num_ciudades_ruta = len(ruta)
    
    for i in range(num_ciudades_ruta):
        c1 = ruta[i]
        # La siguiente ciudad, con 'wrap-around' (la última vuelve a la primera)
        c2 = ruta[(i + 1) % num_ciudades_ruta] 
        costo_total += dist(c1, c2)
        
    return costo_total

def generar_vecino(ruta):
    """
    Genera una ruta vecina usando un '2-opt swap'.
    1. Elige dos índices aleatorios i, j.
    2. Invierte el segmento de la ruta entre i y j.
    """
    # Copia la ruta actual para no modificar la original
    vecino = ruta[:]
    
    # Elige dos índices distintos
    i, j = random.sample(range(len(vecino)), 2)
    
    # Asegura que i < j para el slicing
    if i > j:
        i, j = j, i
        
    # El segmento a invertir es de i hasta j (inclusive)
    # Ej: [A, B, C, D, E] con i=1, j=3 -> segmento [B, C, D]
    segmento = vecino[i : j + 1]
    segmento.reverse()
    
    # Reemplaza el segmento original por el segmento invertido
    vecino[i : j + 1] = segmento
    
    return vecino

def generar_solucion_inicial():
    """Genera una ruta inicial aleatoria (barajando las ciudades)."""
    ruta_ini = lista_ciudades[:] # Copia la lista
    random.shuffle(ruta_ini)
    return ruta_ini


# --- Funciones de Visualización ---

def mostrar_mapa_ciudades():
    """Muestra un mapa con todas las ciudades y sus coordenadas."""
    plt.figure(figsize=(10, 8))
    
    # Extraer coordenadas
    x_coords = [ciudades[ciudad][0] for ciudad in ciudades.keys()]
    y_coords = [ciudades[ciudad][1] for ciudad in ciudades.keys()]
    
    # Dibujar ciudades como puntos
    plt.scatter(x_coords, y_coords, c='red', s=100, alpha=0.7)
    
    # Añadir etiquetas con los nombres de las ciudades
    for ciudad, (x, y) in ciudades.items():
        plt.annotate(ciudad, (x, y), xytext=(5, 5), textcoords='offset points', 
                    fontsize=8, fontweight='bold')  # Fuente más pequeña para nombres de 2 letras
    
    plt.title(f'Mapa de Ciudades - TSP ({NUM_CIUDADES} ciudades)', fontsize=14)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-10, MAPA_SIZE + 10)
    plt.ylim(-10, MAPA_SIZE + 10)
    plt.show()

def mostrar_ruta(ruta, titulo="Ruta", color='blue', mostrar_direccion=True):
    """
    Muestra un mapa con la ruta especificada.
    
    Args:
        ruta: Lista de nombres de ciudades en orden
        titulo: Título del gráfico
        color: Color de las líneas de la ruta
        mostrar_direccion: Si mostrar flechas indicando la dirección
    """
    plt.figure(figsize=(12, 8))
    
    # Extraer coordenadas de todas las ciudades
    x_coords = [ciudades[ciudad][0] for ciudad in ciudades.keys()]
    y_coords = [ciudades[ciudad][1] for ciudad in ciudades.keys()]
    
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
    
    # Añadir etiquetas con los nombres de las ciudades
    for ciudad, (x, y) in ciudades.items():
        plt.annotate(ciudad, (x, y), xytext=(5, 5), textcoords='offset points', 
                    fontsize=7, fontweight='bold')  # Fuente más pequeña para 150 ciudades
    
    # Añadir flechas para mostrar la dirección si se solicita
    if mostrar_direccion:
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
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    
    # Calcular y mostrar el costo de la ruta
    costo = calcular_costo(ruta)
    plt.title(f'{titulo} - Costo: {costo:.2f}', fontsize=14)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-10, MAPA_SIZE + 10)
    plt.ylim(-10, MAPA_SIZE + 10)
    plt.show()

def comparar_rutas(ruta_inicial, ruta_final):
    """Muestra una comparación lado a lado de dos rutas."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Función auxiliar para dibujar una ruta en un subplot específico
    def dibujar_en_subplot(ax, ruta, titulo, color):
        # Todas las ciudades en gris
        x_coords = [ciudades[ciudad][0] for ciudad in ciudades.keys()]
        y_coords = [ciudades[ciudad][1] for ciudad in ciudades.keys()]
        ax.scatter(x_coords, y_coords, c='lightgray', s=80, alpha=0.5)
        
        # Ruta específica
        ruta_x = [ciudades[ciudad][0] for ciudad in ruta]
        ruta_y = [ciudades[ciudad][1] for ciudad in ruta]
        ruta_x.append(ruta_x[0])  # Cerrar circuito
        ruta_y.append(ruta_y[0])
        
        ax.plot(ruta_x, ruta_y, color=color, linewidth=2, alpha=0.8)
        ax.scatter(ruta_x[:-1], ruta_y[:-1], c=color, s=120, alpha=0.9)
        
        # Etiquetas (solo mostrar ciudades de la ruta para evitar saturación)
        for ciudad in ruta:
            x, y = ciudades[ciudad]
            ax.annotate(ciudad, (x, y), xytext=(3, 3), textcoords='offset points', 
                       fontsize=6, fontweight='bold', color='white', 
                       bbox=dict(boxstyle="round,pad=0.1", facecolor=color, alpha=0.7))
        
        costo = calcular_costo(ruta)
        ax.set_title(f'{titulo} - Costo: {costo:.2f}', fontsize=12)
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, MAPA_SIZE + 10)
        ax.set_ylim(-10, MAPA_SIZE + 10)
    
    # Dibujar ambas rutas
    dibujar_en_subplot(ax1, ruta_inicial, "Ruta Inicial", 'red')
    dibujar_en_subplot(ax2, ruta_final, "Ruta Optimizada", 'green')
    
    plt.tight_layout()
    plt.show()

def mostrar_info_ciudades():
    """Muestra información detallada de todas las ciudades y sus distancias."""
    print("\n=== INFORMACIÓN DETALLADA DE CIUDADES ===")
    print(f"Total de ciudades: {len(ciudades)}")
    print(f"Área del mapa: {MAPA_SIZE} x {MAPA_SIZE}")
    print("\nCoordenadas de las ciudades:")
    for ciudad, (x, y) in sorted(ciudades.items()):
        print(f"  {ciudad}: ({x:3d}, {y:3d})")
    
    print("\nMatriz de distancias (muestra parcial):")
    nombres = sorted(ciudades.keys())[:6]  # Primeras 6 ciudades para mostrar formato
    print("     ", end="")  # Espacio para el header
    for nombre in nombres:
        print(f"{nombre:9s}", end="")  # Más espacio para nombres de 2 letras
    print()
    
    for i, ciudad1 in enumerate(nombres):
        print(f"{ciudad1:4s} ", end="")  # Espacio para nombres de 2 letras
        for j, ciudad2 in enumerate(nombres):
            if i <= j:
                distancia = dist(ciudad1, ciudad2)
                print(f"{distancia:8.1f} ", end="")
            else:
                print(f"{'':9s}", end="")
        print()
    
    if len(ciudades) > 5:
        print("  ... (matriz completa omitida para claridad)")
    print("="*50)

def guardar_visualizaciones(ruta_inicial, ruta_final, prefijo_archivo="tsp_resultado"):
    """
    Guarda las visualizaciones como archivos de imagen.
    
    Args:
        ruta_inicial: Ruta inicial del algoritmo
        ruta_final: Ruta optimizada final
        prefijo_archivo: Prefijo para los nombres de archivo
    """
    # Guardar mapa de ciudades (sin etiquetas para 150 ciudades)
    plt.figure(figsize=(12, 10))
    x_coords = [ciudades[ciudad][0] for ciudad in ciudades.keys()]
    y_coords = [ciudades[ciudad][1] for ciudad in ciudades.keys()]
    plt.scatter(x_coords, y_coords, c='red', s=30, alpha=0.6)  # Puntos más pequeños
    
    # No mostrar todas las etiquetas para evitar saturación con 150 ciudades
    # Solo mostrar algunas ciudades como referencia
    ciudades_muestra = list(ciudades.keys())[::10]  # Cada 10 ciudades
    for ciudad in ciudades_muestra:
        x, y = ciudades[ciudad]
        plt.annotate(ciudad, (x, y), xytext=(2, 2), textcoords='offset points', 
                    fontsize=6, fontweight='bold')
    
    plt.title(f'Mapa de Ciudades - TSP ({NUM_CIUDADES} ciudades)', fontsize=14)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-10, MAPA_SIZE + 10)
    plt.ylim(-10, MAPA_SIZE + 10)
    plt.savefig(f'{prefijo_archivo}_mapa_ciudades.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Guardar comparación de rutas
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    def dibujar_en_subplot_para_guardar(ax, ruta, titulo, color):
        x_coords = [ciudades[ciudad][0] for ciudad in ciudades.keys()]
        y_coords = [ciudades[ciudad][1] for ciudad in ciudades.keys()]
        ax.scatter(x_coords, y_coords, c='lightgray', s=15, alpha=0.3)  # Puntos más pequeños
        
        ruta_x = [ciudades[ciudad][0] for ciudad in ruta]
        ruta_y = [ciudades[ciudad][1] for ciudad in ruta]
        ruta_x.append(ruta_x[0])
        ruta_y.append(ruta_y[0])
        
        ax.plot(ruta_x, ruta_y, color=color, linewidth=2, alpha=0.8)
        ax.scatter(ruta_x[:-1], ruta_y[:-1], c=color, s=30, alpha=0.9)  # Puntos más pequeños
        
        # No mostrar etiquetas individuales para 150 ciudades
        # Solo mostrar algunos puntos clave en la ruta
        puntos_clave = ruta[::max(1, len(ruta)//10)]  # Mostrar cada N ciudades de la ruta
        for ciudad in puntos_clave:
            x, y = ciudades[ciudad]
            ax.annotate(ciudad, (x, y), xytext=(2, 2), textcoords='offset points', 
                       fontsize=5, fontweight='bold', color='white',
                       bbox={'boxstyle': "round,pad=0.1", 'facecolor': color, 'alpha': 0.7})
        
        costo = calcular_costo(ruta)
        ax.set_title(f'{titulo} - Costo: {costo:.2f}', fontsize=12)
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, MAPA_SIZE + 10)
        ax.set_ylim(-10, MAPA_SIZE + 10)
    
    dibujar_en_subplot_para_guardar(ax1, ruta_inicial, "Ruta Inicial", 'red')
    dibujar_en_subplot_para_guardar(ax2, ruta_final, "Ruta Optimizada", 'green')
    
    plt.tight_layout()
    plt.savefig(f'{prefijo_archivo}_comparacion.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n📁 Visualizaciones guardadas:")
    print(f"   - {prefijo_archivo}_mapa_ciudades.png")
    print(f"   - {prefijo_archivo}_comparacion.png")


def comparar_topologias(num_ciudades, mapa_size, T_ini, T_fin, ratio_enfriamiento):
    """
    Compara el rendimiento del algoritmo en diferentes topologías de ciudades.
    
    Args:
        num_ciudades: Número de ciudades
        mapa_size: Tamaño del mapa
        T_ini, T_fin, ratio_enfriamiento: Parámetros del algoritmo SA
    
    Returns:
        dict: Resultados de la comparación
    """
    global ciudades, lista_ciudades
    
    resultados = {}
    topologias = {
        'Uniforme': generar_ciudades_uniformes,
        'Clusters': generar_ciudades_clusters,
        'Aleatoria': generar_ciudades_aleatorias
    }
    
    print("="*80)
    print(f"COMPARACIÓN DE TOPOLOGÍAS - {num_ciudades} ciudades")
    print("="*80)
    
    for nombre_topologia, funcion_generadora in topologias.items():
        print(f"\n--- Ejecutando: {nombre_topologia} ---")
        
        # Generar ciudades según la topología
        ciudades = funcion_generadora(num_ciudades, mapa_size)
        lista_ciudades = list(ciudades.keys())
        
        # Generar solución inicial
        sol_inicial = generar_solucion_inicial()
        costo_inicial = calcular_costo(sol_inicial)
        
        print(f"Costo inicial: {costo_inicial:.2f}")
        
        # Ejecutar Simulated Annealing
        mejor_sol, mejor_costo = simulated_annealing(
            sol_inicial, T_ini, T_fin, ratio_enfriamiento
        )
        
        # Calcular mejora
        mejora_porcentual = ((costo_inicial - mejor_costo) / costo_inicial) * 100
        
        # Guardar resultados
        resultados[nombre_topologia] = {
            'ciudades': dict(ciudades),  # Copia de las ciudades
            'ruta_inicial': sol_inicial[:],
            'ruta_final': mejor_sol[:],
            'costo_inicial': costo_inicial,
            'costo_final': mejor_costo,
            'mejora_porcentual': mejora_porcentual
        }
        
        print(f"Costo final: {mejor_costo:.2f}")
        print(f"Mejora: {mejora_porcentual:.2f}%")
    
    return resultados

def visualizar_comparacion_topologias(resultados):
    """
    Crea visualizaciones comparativas de las diferentes topologías.
    """
    num_topologias = len(resultados)
    fig, axes = plt.subplots(2, num_topologias, figsize=(6*num_topologias, 12))
    
    if num_topologias == 1:
        axes = axes.reshape(2, 1)
    
    for i, (nombre_topologia, datos) in enumerate(resultados.items()):
        ciudades_temp = datos['ciudades']
        
        # Fila superior: Distribución de ciudades y ruta inicial
        ax_superior = axes[0, i]
        x_coords = [ciudades_temp[ciudad][0] for ciudad in ciudades_temp.keys()]
        y_coords = [ciudades_temp[ciudad][1] for ciudad in ciudades_temp.keys()]
        
        ax_superior.scatter(x_coords, y_coords, c='lightcoral', s=30, alpha=0.6, label='Ciudades')
        
        # Dibujar ruta inicial
        ruta_inicial = datos['ruta_inicial']
        ruta_x = [ciudades_temp[ciudad][0] for ciudad in ruta_inicial]
        ruta_y = [ciudades_temp[ciudad][1] for ciudad in ruta_inicial]
        ruta_x.append(ruta_x[0])
        ruta_y.append(ruta_y[0])
        
        ax_superior.plot(ruta_x, ruta_y, 'r-', linewidth=1, alpha=0.7, label='Ruta Inicial')
        ax_superior.set_title(f'{nombre_topologia}\nInicial: {datos["costo_inicial"]:.1f}', fontsize=11)
        ax_superior.grid(True, alpha=0.3)
        ax_superior.legend(fontsize=8)
        
        # Fila inferior: Ruta optimizada
        ax_inferior = axes[1, i]
        ax_inferior.scatter(x_coords, y_coords, c='lightblue', s=30, alpha=0.6, label='Ciudades')
        
        # Dibujar ruta optimizada
        ruta_final = datos['ruta_final']
        ruta_x = [ciudades_temp[ciudad][0] for ciudad in ruta_final]
        ruta_y = [ciudades_temp[ciudad][1] for ciudad in ruta_final]
        ruta_x.append(ruta_x[0])
        ruta_y.append(ruta_y[0])
        
        ax_inferior.plot(ruta_x, ruta_y, 'g-', linewidth=2, alpha=0.8, label='Ruta Optimizada')
        ax_inferior.set_title(f'Optimizada: {datos["costo_final"]:.1f}\nMejora: {datos["mejora_porcentual"]:.1f}%', 
                             fontsize=11)
        ax_inferior.grid(True, alpha=0.3)
        ax_inferior.legend(fontsize=8)
        
        # Configurar límites iguales para todos los subplots
        for ax in [ax_superior, ax_inferior]:
            ax.set_xlim(-10, MAPA_SIZE + 10)
            ax.set_ylim(-10, MAPA_SIZE + 10)
            ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    plt.savefig('comparacion_topologias.png', dpi=300, bbox_inches='tight')
    plt.show()

def mostrar_estadisticas_comparacion(resultados):
    """
    Muestra estadísticas detalladas de la comparación.
    """
    print("\n" + "="*80)
    print("ESTADÍSTICAS DE COMPARACIÓN")
    print("="*80)
    
    # Crear tabla de resultados
    print(f"{'Topología':<12} {'Costo Inicial':<15} {'Costo Final':<13} {'Mejora (%)':<12} {'Eficiencia':<12}")
    print("-" * 70)
    
    mejor_topologia = None
    mejor_costo = float('inf')
    mejor_mejora = 0
    
    for nombre, datos in resultados.items():
        eficiencia = datos['mejora_porcentual'] / datos['costo_inicial'] * 1000  # Métrica de eficiencia
        
        print(f"{nombre:<12} {datos['costo_inicial']:<15.1f} {datos['costo_final']:<13.1f} "
              f"{datos['mejora_porcentual']:<12.1f} {eficiencia:<12.2f}")
        
        if datos['costo_final'] < mejor_costo:
            mejor_costo = datos['costo_final']
            mejor_topologia = nombre
        
        if datos['mejora_porcentual'] > mejor_mejora:
            mejor_mejora = datos['mejora_porcentual']
    
    print("-" * 70)
    print(f"\n🏆 MEJOR RESULTADO: {mejor_topologia} (Costo final: {mejor_costo:.1f})")
    print(f"📈 MAYOR MEJORA: {mejor_mejora:.1f}%")
    
    # Análisis adicional
    print(f"\n📊 ANÁLISIS:")
    costos_finales = [datos['costo_final'] for datos in resultados.values()]
    mejoras = [datos['mejora_porcentual'] for datos in resultados.values()]
    
    print(f"   • Diferencia entre mejor y peor costo final: {max(costos_finales) - min(costos_finales):.1f}")
    print(f"   • Mejora promedio: {sum(mejoras) / len(mejoras):.1f}%")
    print(f"   • Desviación en mejoras: {max(mejoras) - min(mejoras):.1f}%")


# --- 2. Algoritmo de Simulated Annealing (Idéntico) ---
# Esta función es la misma, es genérica.

def simulated_annealing(solucion_inicial, T_inicial, T_min, alfa):
    T = T_inicial
    solucion_actual = solucion_inicial
    costo_actual = calcular_costo(solucion_actual)
    
    mejor_solucion = solucion_actual
    mejor_costo = costo_actual
    
    iteracion = 0
    
    while T > T_min:
        # 1. Generar un vecino
        solucion_vecina = generar_vecino(solucion_actual)
        costo_vecino = calcular_costo(solucion_vecina)

        # 2. Calcular la diferencia de costo
        delta_costo = costo_vecino - costo_actual

        # 3. Decidir si nos movemos
        if delta_costo < 0:
            # Es mejor, aceptamos
            solucion_actual = solucion_vecina
            costo_actual = costo_vecino
        else:
            # Es peor, aceptamos con probabilidad
            probabilidad = math.exp(-delta_costo / T)
            if random.random() < probabilidad:
                solucion_actual = solucion_vecina
                costo_actual = costo_vecino
        
        # 4. Actualizar la mejor solución global
        if costo_actual < mejor_costo:
            mejor_solucion = solucion_actual
            mejor_costo = costo_actual
            
        # 5. Enfriar
        T *= alfa
        
        # Opcional: Imprimir progreso
        if iteracion % 5000 == 0:
            print(f"T: {T:6.2f} | Costo Actual: {costo_actual:8.2f} | Mejor Costo: {mejor_costo:8.2f}")
        iteracion += 1

    return mejor_solucion, mejor_costo


# --- 3. Ejecución del Caso de Prueba (TSP) ---

if __name__ == "__main__":
    
    # Parámetros de SA (TSP es complejo, necesita enfriamiento lento)
    T_ini = 1000.0          # Temperatura inicial alta
    T_fin = 0.1             # Temperatura final muy baja
    ratio_enfriamiento = 0.9995 # Enfriamiento muy lento (más cerca de 1)

    # Configuración del experimento
    MODO_COMPARACION = True  # Cambiar a False para ejecutar solo una topología
    
    if MODO_COMPARACION:
        # === MODO COMPARACIÓN DE TOPOLOGÍAS ===
        print("\n🔬 MODO COMPARACIÓN DE TOPOLOGÍAS ACTIVADO")
        print("Se ejecutará el algoritmo en 3 topologías diferentes:\n")
        print("1. 📐 Uniforme: Ciudades distribuidas en cuadrícula con variación")
        print("2. 🎯 Clusters: Ciudades agrupadas en clusters aleatorios") 
        print("3. 🎲 Aleatoria: Distribución completamente aleatoria\n")
        
        # Usar menos ciudades para comparación más rápida
        num_ciudades_comparacion = 30
        print(f"Usando {num_ciudades_comparacion} ciudades para la comparación...")
        
        # Ejecutar comparación
        resultados = comparar_topologias(
            num_ciudades_comparacion, 
            MAPA_SIZE, 
            T_ini, 
            T_fin, 
            ratio_enfriamiento
        )
        
        # Mostrar estadísticas
        mostrar_estadisticas_comparacion(resultados)
        
        # Crear visualizaciones comparativas
        print("\n📊 Generando visualizaciones comparativas...")
        visualizar_comparacion_topologias(resultados)
        
        print("\n✅ Comparación completada. Revisa 'comparacion_topologias.png'")
        
    else:
        # === MODO EJECUCIÓN INDIVIDUAL ===
        # Seleccionar tipo de topología (puedes cambiar aquí)
        TIPO_TOPOLOGIA = "clusters"  # opciones: "uniforme", "clusters", "aleatoria"
        NUM_CIUDADES = 30  # Reducir para demostración más rápida
        
        # Generar ciudades según el tipo seleccionado
        if TIPO_TOPOLOGIA == "uniforme":
            ciudades = generar_ciudades_uniformes(NUM_CIUDADES, MAPA_SIZE)
            print(f"🔹 Usando topología UNIFORME con {NUM_CIUDADES} ciudades")
        elif TIPO_TOPOLOGIA == "clusters":
            ciudades = generar_ciudades_clusters(NUM_CIUDADES, MAPA_SIZE)
            print(f"🔸 Usando topología de CLUSTERS con {NUM_CIUDADES} ciudades")
        else:  # aleatoria
            ciudades = generar_ciudades_aleatorias(NUM_CIUDADES, MAPA_SIZE)
            print(f"🔹 Usando topología ALEATORIA con {NUM_CIUDADES} ciudades")
        
        lista_ciudades = list(ciudades.keys())

        # 1. Crear solución inicial
        sol_inicial = generar_solucion_inicial()
        costo_inicial = calcular_costo(sol_inicial)

        print(f"\n--- Problema: Viajante de Comercio ({NUM_CIUDADES} ciudades) ---")
        
        # Mostrar información detallada de las ciudades
        mostrar_info_ciudades()
        
        print(f"Ruta Inicial: {' -> '.join(sol_inicial)} -> {sol_inicial[0]}")
        print(f"Costo Inicial: {costo_inicial:.2f}\n")
        
        # Mostrar mapa de ciudades
        print("Mostrando mapa de ciudades...")
        mostrar_mapa_ciudades()
        
        # Mostrar ruta inicial
        print("Mostrando ruta inicial...")
        mostrar_ruta(sol_inicial, "Ruta Inicial", 'red')
        
        print("Iniciando Simulated Annealing...\n")

        # 2. Ejecutar el algoritmo
        mejor_sol, mejor_cost = simulated_annealing(
            sol_inicial, 
            T_ini, 
            T_fin, 
            ratio_enfriamiento
        )

        # 3. Mostrar resultado
        print("\n--- Resultado Final ---")
        print(f"Mejor Ruta: {' -> '.join(mejor_sol)} -> {mejor_sol[0]}")
        print(f"Costo Inicial: {costo_inicial:.2f}")
        print(f"Mejor Costo:   {mejor_cost:.2f}")
        print(f"Mejora: {((costo_inicial - mejor_cost) / costo_inicial) * 100:.2f}%")
        
        # Mostrar visualizaciones finales
        print("\nMostrando ruta optimizada...")
        mostrar_ruta(mejor_sol, "Ruta Optimizada (Simulated Annealing)", 'green')
        
        print("\nComparando rutas inicial vs optimizada...")
        comparar_rutas(sol_inicial, mejor_sol)
        
        # Guardar las visualizaciones como archivos
        print("\nGuardando visualizaciones...")
        guardar_visualizaciones(sol_inicial, mejor_sol)
