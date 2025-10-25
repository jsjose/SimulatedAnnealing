"""
Ejemplo de uso del sistema de comparación de formulaciones TSP

Este script demuestra cómo usar el comparador de formulaciones
para evaluar el rendimiento de diferentes enfoques al TSP.
"""

from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

def ejemplo_comparacion_rapida():
    """
    Ejemplo rápido de comparación con parámetros optimizados para velocidad.
    """
    print("🚀 EJEMPLO RÁPIDO DE COMPARACIÓN")
    print("="*50)
    
    # Configuración rápida
    num_ciudades = 6  # Número pequeño para pruebas rápidas
    ciudades = tsp.generar_ciudades_uniformes(num_ciudades, 100)
    
    print(f"Ciudades generadas: {list(ciudades.keys())}")
    
    # Parámetros de SA rápidos
    sa_params_rapido = {
        'initial_temperature': 100.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.95,
        'verbose': False,
        'progress_interval': 100
    }
    
    # Crear comparador y ejecutar
    comparador = TSPFormulationComparator(ciudades)
    resultado = comparador.compare_single_run(sa_params_rapido, verbose=True)
    
    return resultado

def ejemplo_comparacion_detallada():
    """
    Ejemplo detallado con análisis completo y visualizaciones.
    """
    print("🔬 EJEMPLO DETALLADO DE COMPARACIÓN")
    print("="*50)
    
    # Configuración para análisis detallado
    num_ciudades = 8
    ciudades = tsp.generar_ciudades_clusters(num_ciudades, 150, num_clusters=2)
    
    # Mostrar mapa inicial
    tsp.mostrar_mapa_ciudades(ciudades, "Ciudades para Análisis Detallado")
    
    # Parámetros de SA más exhaustivos
    sa_params_detallado = {
        'initial_temperature': 500.0,
        'final_temperature': 0.01,
        'cooling_rate': 0.99,
        'verbose': True,
        'progress_interval': 500
    }
    
    # Crear comparador
    comparador = TSPFormulationComparator(ciudades)
    
    # Ejecutar comparación única
    print("\n🔍 ANÁLISIS INDIVIDUAL...")
    resultado = comparador.compare_single_run(sa_params_detallado)
    
    # Visualizar resultados
    print("\n📊 GENERANDO VISUALIZACIONES...")
    comparador.visualize_comparison(resultado)
    
    # Análisis estadístico
    print("\n📈 ANÁLISIS ESTADÍSTICO...")
    estadisticas = comparador.compare_multiple_runs(sa_params_detallado, num_runs=3)
    comparador.visualize_statistics(estadisticas)
    
    return resultado, estadisticas

def ejemplo_analisis_escalabilidad():
    """
    Análisis de cómo escalan las formulaciones con el número de ciudades.
    """
    print("📈 ANÁLISIS DE ESCALABILIDAD")
    print("="*50)
    
    tamanos = [4, 6, 8]  # Tamaños de problema para análisis
    resultados_escalabilidad = []
    
    # Parámetros constantes
    sa_params = {
        'initial_temperature': 200.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.98,
        'verbose': False
    }
    
    for n in tamanos:
        print(f"\n--- Analizando {n} ciudades ---")
        
        # Generar problema
        ciudades = tsp.generar_ciudades_uniformes(n, 100)
        comparador = TSPFormulationComparator(ciudades)
        
        # Ejecutar comparación
        resultado = comparador.compare_single_run(sa_params, verbose=False)
        
        # Guardar métricas clave
        escalabilidad = {
            'num_ciudades': n,
            'time_classical': resultado['comparison']['time_classical'],
            'time_qubo': resultado['comparison']['time_qubo'],
            'time_ratio': resultado['comparison']['time_ratio'],
            'cost_classical': resultado['comparison']['tour_cost_classical'],
            'cost_qubo': resultado['comparison']['tour_cost_qubo'],
            'qubo_valid': resultado['comparison']['qubo_valid']
        }
        
        resultados_escalabilidad.append(escalabilidad)
        
        print(f"  Tiempo clásico: {escalabilidad['time_classical']:.2f}s")
        print(f"  Tiempo QUBO: {escalabilidad['time_qubo']:.2f}s")
        print(f"  Ratio tiempo: {escalabilidad['time_ratio']:.2f}x")
        print(f"  QUBO válido: {escalabilidad['qubo_valid']}")
    
    # Mostrar resumen de escalabilidad
    print(f"\n{'='*50}")
    print("RESUMEN DE ESCALABILIDAD")
    print(f"{'='*50}")
    print(f"{'Ciudades':<10} {'T.Clás(s)':<10} {'T.QUBO(s)':<10} {'Ratio':<8} {'Válido':<8}")
    print("-" * 50)
    
    for r in resultados_escalabilidad:
        print(f"{r['num_ciudades']:<10} {r['time_classical']:<10.2f} {r['time_qubo']:<10.2f} "
              f"{r['time_ratio']:<8.1f} {'Sí' if r['qubo_valid'] else 'No':<8}")
    
    return resultados_escalabilidad

if __name__ == "__main__":
    print("🧪 EJEMPLOS DE COMPARACIÓN TSP: CLÁSICO vs QUBO\n")
    
    # Menú de ejemplos
    print("Selecciona un ejemplo:")
    print("1. Comparación rápida (6 ciudades)")
    print("2. Análisis detallado (8 ciudades)")
    print("3. Análisis de escalabilidad")
    print("4. Ejecutar todos los ejemplos")
    
    opcion = input("\nElige una opción (1-4): ").strip()
    
    if opcion == "1":
        ejemplo_comparacion_rapida()
    elif opcion == "2":
        ejemplo_comparacion_detallada()
    elif opcion == "3":
        ejemplo_analisis_escalabilidad()
    elif opcion == "4":
        print("\n🚀 Ejecutando comparación rápida...")
        ejemplo_comparacion_rapida()
        
        print("\n" + "="*80)
        print("\n🔬 Ejecutando análisis detallado...")
        ejemplo_comparacion_detallada()
        
        print("\n" + "="*80)
        print("\n📈 Ejecutando análisis de escalabilidad...")
        ejemplo_analisis_escalabilidad()
    else:
        print("Opción no válida. Ejecutando ejemplo rápido por defecto...")
        ejemplo_comparacion_rapida()
    
    print("\n🎉 ¡Ejemplos completados!")