#!/usr/bin/env python3
"""
📈 Análisis de Escalabilidad TSP: Clásico vs QUBO

Demostración exhaustiva que evalúa el rendimiento de ambas formulaciones
del TSP con diferentes números de ciudades (10-150) y genera gráficas
comparativas de costo y tiempo de ejecución.

Autor: Sistema de Optimización Cuántica
Fecha: Octubre 2025
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

def mostrar_banner_escalabilidad():
    """Banner para el análisis de escalabilidad."""
    print("📈" * 60)
    print("🔬 ANÁLISIS DE ESCALABILIDAD TSP: CLÁSICO vs QUBO")
    print("📈" * 60)
    print("🎯 Objetivo: Evaluar rendimiento con 10-150 ciudades")
    print("📊 Métricas: Costo del tour y tiempo de ejecución")
    print("🔍 Intervalos: Cada 10 ciudades (15 puntos de datos)")
    print("📈" * 60)

def ejecutar_analisis_escalabilidad(
    min_ciudades: int = 10,
    max_ciudades: int = 150, 
    intervalo: int = 10,
    topologia: str = "uniformes"
) -> Dict:
    """
    Ejecuta análisis de escalabilidad completo.
    
    Args:
        min_ciudades: Número mínimo de ciudades
        max_ciudades: Número máximo de ciudades  
        intervalo: Intervalo entre puntos de datos
        topologia: Tipo de distribución ("uniformes", "clusters", "aleatorias")
        
    Returns:
        Diccionario con resultados del análisis
    """
    
    # Generar rangos de ciudades
    rangos_ciudades = list(range(min_ciudades, max_ciudades + 1, intervalo))
    num_puntos = len(rangos_ciudades)
    
    print(f"\n🚀 INICIANDO ANÁLISIS DE ESCALABILIDAD")
    print(f"   📊 Puntos de datos: {num_puntos}")
    print(f"   🏙️  Ciudades: {min_ciudades} → {max_ciudades} (intervalo: {intervalo})")
    print(f"   🗺️  Topología: {topologia.capitalize()}")
    print(f"   ⏱️  Tiempo estimado: ~{num_puntos * 0.5:.1f} minutos")
    print("-" * 60)
    
    # Parámetros optimizados de SA para cada rango
    def get_sa_params(n_ciudades: int) -> Dict:
        """Obtiene parámetros SA adaptativos según el tamaño del problema."""
        if n_ciudades <= 20:
            return {
                'initial_temperature': 500.0,
                'final_temperature': 0.1,
                'cooling_rate': 0.97,
                'verbose': False
            }
        elif n_ciudades <= 50:
            return {
                'initial_temperature': 800.0,
                'final_temperature': 0.05,
                'cooling_rate': 0.98,
                'verbose': False
            }
        else:  # > 50 ciudades
            return {
                'initial_temperature': 1200.0,
                'final_temperature': 0.01,
                'cooling_rate': 0.99,
                'verbose': False
            }
    
    # Almacenar resultados
    resultados = {
        'num_ciudades': [],
        'costo_clasico': [],
        'costo_qubo': [],
        'tiempo_clasico': [],
        'tiempo_qubo': [],
        'qubo_valido': [],
        'ratio_tiempo': [],
        'ratio_costo': [],
        'errores': []
    }
    
    # Ejecutar análisis para cada tamaño
    for i, n in enumerate(rangos_ciudades):
        print(f"📊 Procesando {n:3d} ciudades ({i+1:2d}/{num_puntos:2d})... ", end="", flush=True)
        
        try:
            start_time = time.time()
            
            # Generar ciudades según topología
            if topologia == "uniformes":
                ciudades = tsp.generar_ciudades_uniformes(n, 300)
            elif topologia == "clusters":
                num_clusters = max(2, n // 15)  # Adaptar clusters al tamaño
                ciudades = tsp.generar_ciudades_clusters(n, 300, num_clusters)
            else:  # aleatorias
                ciudades = tsp.generar_ciudades_aleatorias(n, 300)
            
            # Configurar parámetros SA
            sa_params = get_sa_params(n)
            
            # Crear comparador y ejecutar
            comparador = TSPFormulationComparator(ciudades)
            resultado = comparador.compare_single_run(sa_params, verbose=False)
            
            # Almacenar resultados
            resultados['num_ciudades'].append(n)
            resultados['costo_clasico'].append(resultado['comparison']['tour_cost_classical'])
            resultados['costo_qubo'].append(resultado['comparison']['tour_cost_qubo'])
            resultados['tiempo_clasico'].append(resultado['comparison']['time_classical'])
            resultados['tiempo_qubo'].append(resultado['comparison']['time_qubo'])
            resultados['qubo_valido'].append(resultado['comparison']['qubo_valid'])
            resultados['ratio_tiempo'].append(resultado['comparison']['time_ratio'])
            resultados['ratio_costo'].append(resultado['comparison']['cost_ratio'])
            
            elapsed = time.time() - start_time
            
            print(f"✅ T_clás: {resultado['comparison']['time_classical']:.3f}s, "
                  f"T_qubo: {resultado['comparison']['time_qubo']:.3f}s, "
                  f"Ratio: {resultado['comparison']['time_ratio']:.1f}x "
                  f"({elapsed:.1f}s total)")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            resultados['errores'].append((n, str(e)))
            # Agregar valores NaN para mantener consistencia
            resultados['num_ciudades'].append(n)
            resultados['costo_clasico'].append(np.nan)
            resultados['costo_qubo'].append(np.nan)
            resultados['tiempo_clasico'].append(np.nan)
            resultados['tiempo_qubo'].append(np.nan)
            resultados['qubo_valido'].append(False)
            resultados['ratio_tiempo'].append(np.nan)
            resultados['ratio_costo'].append(np.nan)
    
    print("-" * 60)
    print(f"✅ Análisis completado: {len([x for x in resultados['costo_clasico'] if not np.isnan(x)])}/{num_puntos} exitosos")
    
    return resultados

def generar_graficas_escalabilidad(resultados: Dict, topologia: str):
    """
    Genera gráficas comparativas de escalabilidad.
    
    Args:
        resultados: Resultados del análisis de escalabilidad
        topologia: Tipo de topología utilizada
    """
    
    print(f"\n📊 GENERANDO GRÁFICAS DE ESCALABILIDAD")
    print("-" * 40)
    
    # Filtrar datos válidos (sin NaN)
    datos_validos = []
    for i in range(len(resultados['num_ciudades'])):
        if not (np.isnan(resultados['costo_clasico'][i]) or np.isnan(resultados['costo_qubo'][i])):
            datos_validos.append(i)
    
    if not datos_validos:
        print("❌ No hay datos válidos para graficar")
        return
    
    # Extraer datos válidos
    ciudades = [resultados['num_ciudades'][i] for i in datos_validos]
    costo_clasico = [resultados['costo_clasico'][i] for i in datos_validos]
    costo_qubo = [resultados['costo_qubo'][i] for i in datos_validos]
    tiempo_clasico = [resultados['tiempo_clasico'][i] for i in datos_validos]
    tiempo_qubo = [resultados['tiempo_qubo'][i] for i in datos_validos]
    
    # Crear figura con 4 subgráficas
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Análisis de Escalabilidad TSP: Clásico vs QUBO\nTopología: {topologia.capitalize()}', 
                 fontsize=16, fontweight='bold')
    
    # Gráfica 1: Costo vs Número de Ciudades
    ax1.plot(ciudades, costo_clasico, 'o-', color='blue', linewidth=2, markersize=6, 
             label='Clásico', alpha=0.8)
    ax1.plot(ciudades, costo_qubo, 's-', color='red', linewidth=2, markersize=6, 
             label='QUBO', alpha=0.8)
    ax1.set_xlabel('Número de Ciudades')
    ax1.set_ylabel('Costo del Tour')
    ax1.set_title('Costo vs Número de Ciudades')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    
    # Gráfica 2: Tiempo vs Número de Ciudades
    ax2.plot(ciudades, tiempo_clasico, 'o-', color='blue', linewidth=2, markersize=6, 
             label='Clásico', alpha=0.8)
    ax2.plot(ciudades, tiempo_qubo, 's-', color='red', linewidth=2, markersize=6, 
             label='QUBO', alpha=0.8)
    ax2.set_xlabel('Número de Ciudades')
    ax2.set_ylabel('Tiempo de Ejecución (segundos)')
    ax2.set_title('Tiempo vs Número de Ciudades')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    ax2.set_yscale('log')  # Escala logarítmica para mejor visualización
    
    # Gráfica 3: Ratio de Tiempos (QUBO/Clásico)
    ratios_tiempo = [tiempo_qubo[i] / tiempo_clasico[i] if tiempo_clasico[i] > 0 else np.nan 
                     for i in range(len(ciudades))]
    ax3.plot(ciudades, ratios_tiempo, 'o-', color='orange', linewidth=2, markersize=6)
    ax3.set_xlabel('Número de Ciudades')
    ax3.set_ylabel('Ratio de Tiempo (QUBO/Clásico)')
    ax3.set_title('Sobrecarga Temporal de QUBO')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    ax3.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Igual rendimiento')
    ax3.legend()
    
    # Gráfica 4: Diferencia Relativa de Costos
    diff_relativa = [(costo_qubo[i] - costo_clasico[i]) / costo_clasico[i] * 100 
                     if costo_clasico[i] > 0 else np.nan for i in range(len(ciudades))]
    ax4.plot(ciudades, diff_relativa, 'o-', color='green', linewidth=2, markersize=6)
    ax4.set_xlabel('Número de Ciudades')
    ax4.set_ylabel('Diferencia Relativa de Costo (%)')
    ax4.set_title('Diferencia de Calidad: (QUBO-Clásico)/Clásico × 100%')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Igual calidad')
    ax4.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Guardar gráfica
    nombre_archivo = f'escalabilidad_tsp_{topologia}_{min(ciudades)}_{max(ciudades)}.png'
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"📁 Gráfica guardada como: {nombre_archivo}")

def mostrar_estadisticas_escalabilidad(resultados: Dict):
    """
    Muestra estadísticas resumidas del análisis de escalabilidad.
    
    Args:
        resultados: Resultados del análisis
    """
    
    print(f"\n📊 ESTADÍSTICAS DE ESCALABILIDAD")
    print("=" * 60)
    
    # Filtrar datos válidos
    datos_validos = []
    for i in range(len(resultados['num_ciudades'])):
        if not np.isnan(resultados['tiempo_clasico'][i]):
            datos_validos.append(i)
    
    if not datos_validos:
        print("❌ No hay datos válidos para estadísticas")
        return
    
    ciudades = [resultados['num_ciudades'][i] for i in datos_validos]
    tiempos_clasico = [resultados['tiempo_clasico'][i] for i in datos_validos]
    tiempos_qubo = [resultados['tiempo_qubo'][i] for i in datos_validos]
    ratios = [resultados['ratio_tiempo'][i] for i in datos_validos]
    
    print(f"📈 Rango analizado: {min(ciudades)} - {max(ciudades)} ciudades")
    print(f"📊 Puntos de datos válidos: {len(datos_validos)}")
    print(f"❌ Errores encontrados: {len(resultados['errores'])}")
    
    print(f"\n⏱️  ANÁLISIS DE TIEMPOS:")
    print(f"   Clásico - Promedio: {np.mean(tiempos_clasico):.3f}s, Máximo: {max(tiempos_clasico):.3f}s")
    print(f"   QUBO    - Promedio: {np.mean(tiempos_qubo):.3f}s, Máximo: {max(tiempos_qubo):.3f}s")
    print(f"   Ratio   - Promedio: {np.mean(ratios):.2f}x, Máximo: {max(ratios):.2f}x")
    
    # Análisis de validez QUBO
    validez_qubo = [resultados['qubo_valido'][i] for i in datos_validos]
    tasa_validez = sum(validez_qubo) / len(validez_qubo) * 100
    print(f"\n✅ VALIDEZ DE SOLUCIONES QUBO:")
    print(f"   Tasa de validez: {tasa_validez:.1f}% ({sum(validez_qubo)}/{len(validez_qubo)})")
    
    # Mostrar errores si los hay
    if resultados['errores']:
        print(f"\n❌ ERRORES ENCONTRADOS:")
        for n_ciudades, error in resultados['errores']:
            print(f"   {n_ciudades} ciudades: {error}")

def main_escalabilidad():
    """Función principal del análisis de escalabilidad."""
    
    mostrar_banner_escalabilidad()
    
    # Configuración del análisis
    print(f"\n⚙️  CONFIGURACIÓN DEL ANÁLISIS")
    print("-" * 40)
    
    # Permitir al usuario elegir parámetros
    print("Selecciona la topología de ciudades:")
    print("1. Uniformes (distribución regular)")
    print("2. Clusters (ciudades agrupadas)")
    print("3. Aleatorias (distribución aleatoria)")
    
    try:
        opcion = input("Elige una opción (1-3, default=1): ").strip()
        if opcion == "2":
            topologia = "clusters"
        elif opcion == "3":
            topologia = "aleatorias"
        else:
            topologia = "uniformes"
    except:
        topologia = "uniformes"
    
    # Confirmar parámetros
    min_ciudades = 10
    max_ciudades = 150
    intervalo = 10
    
    print(f"\n🎯 Parámetros del análisis:")
    print(f"   Topología: {topologia.capitalize()}")
    print(f"   Rango: {min_ciudades}-{max_ciudades} ciudades")
    print(f"   Intervalo: {intervalo} ciudades")
    print(f"   Puntos de datos: {len(range(min_ciudades, max_ciudades + 1, intervalo))}")
    
    confirmar = input(f"\n¿Proceder con el análisis? (y/N): ").strip().lower()
    if confirmar != 'y':
        print("Análisis cancelado.")
        return
    
    # Ejecutar análisis
    print(f"\n🚀 Iniciando análisis de escalabilidad...")
    
    start_time = time.time()
    resultados = ejecutar_analisis_escalabilidad(
        min_ciudades=min_ciudades,
        max_ciudades=max_ciudades,
        intervalo=intervalo,
        topologia=topologia
    )
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Análisis completado en {total_time/60:.1f} minutos")
    
    # Mostrar estadísticas
    mostrar_estadisticas_escalabilidad(resultados)
    
    # Generar gráficas
    generar_graficas_escalabilidad(resultados, topologia)
    
    print(f"\n🎉 ANÁLISIS DE ESCALABILIDAD COMPLETADO")
    print("=" * 60)
    print("📊 Se han generado gráficas comparativas de:")
    print("   • Costo vs Número de Ciudades")
    print("   • Tiempo vs Número de Ciudades") 
    print("   • Ratio de Tiempos (QUBO/Clásico)")
    print("   • Diferencia Relativa de Costos")
    print("\n📁 Los resultados se han guardado como archivo PNG")
    print("🔬 Usa estos datos para evaluar la escalabilidad práctica de QUBO vs Clásico")

if __name__ == "__main__":
    try:
        main_escalabilidad()
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        print("👋 ¡Los datos parciales se pueden recuperar!")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        print("🔧 Verifica que todas las dependencias estén instaladas")
        import traceback
        traceback.print_exc()