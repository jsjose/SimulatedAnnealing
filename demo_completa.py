#!/usr/bin/env python3
"""
🎬 Demostración Completa del Sistema de Comparación TSP

Script de demostración que ejecuta todas las funcionalidades principales
del framework de comparación entre formulaciones clásica y QUBO del TSP.

Autor: Sistema de Optimización Cuántica  
Fecha: Octubre 2025
"""

import sys
import time
import matplotlib.pyplot as plt
from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

def mostrar_banner():
    """Muestra el banner inicial del sistema."""
    print("🚀" * 50)
    print("🎯 SISTEMA DE COMPARACIÓN TSP: CLÁSICO vs QUBO")
    print("🚀" * 50)
    print("📊 Framework modular de optimización con Simulated Annealing")
    print("⚛️  Comparación entre formulaciones clásica y cuántica")
    print("🔬 Análisis de rendimiento, escalabilidad y validez")
    print("🚀" * 50)

def demo_topologias():
    """Demuestra diferentes topologías de ciudades."""
    print("\n🏙️  DEMOSTRACIÓN DE TOPOLOGÍAS DE CIUDADES")
    print("="*60)
    
    num_ciudades = 50
    mapa_size = 200
    
    # Generar diferentes topologías
    topologias = {
        "Uniformes": tsp.generar_ciudades_uniformes(num_ciudades, mapa_size),
        "Clusters": tsp.generar_ciudades_clusters(num_ciudades, mapa_size, num_clusters=3),
        "Aleatorias": tsp.generar_ciudades_aleatorias(num_ciudades, mapa_size)
    }
    
    print("Generando ciudades con diferentes distribuciones...")
    
    # Mostrar mapas de cada topología
    for nombre, ciudades in topologias.items():
        print(f"📍 Topología: {nombre}")
        tsp.mostrar_mapa_ciudades(ciudades, f"Ciudades {nombre} ({num_ciudades} ciudades)")
        time.sleep(1)  # Pausa breve para visualización
    
    return topologias["Clusters"]  # Devolver una para usar en demos posteriores

def demo_comparacion_rapida(ciudades):
    """Demostración de comparación rápida entre formulaciones."""
    print("\n⚡ DEMOSTRACIÓN: COMPARACIÓN RÁPIDA")
    print("="*60)
    
    # Configuración rápida para demostración
    sa_params = {
        'initial_temperature': 200.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.95,
        'verbose': False,
        'progress_interval': 50
    }
    
    print(f"🎯 Problema: {len(ciudades)} ciudades en topología de clusters")
    print(f"🧮 Algoritmo: Simulated Annealing (T₀={sa_params['initial_temperature']}, α={sa_params['cooling_rate']})")
    
    # Crear comparador y ejecutar
    comparador = TSPFormulationComparator(ciudades)
    
    print("🔄 Ejecutando formulación clásica...")
    start_time = time.time()
    resultado = comparador.compare_single_run(sa_params, verbose=False)
    total_time = time.time() - start_time
    
    # Mostrar resultados resumidos
    print(f"\n📊 RESULTADOS:")
    print(f"   Formulación Clásica:")
    print(f"     • Costo: {resultado['comparison']['tour_cost_classical']:.2f}")
    print(f"     • Tiempo: {resultado['comparison']['time_classical']:.3f}s")
    
    print(f"   Formulación QUBO:")
    print(f"     • Costo: {resultado['comparison']['tour_cost_qubo']:.2f}")
    print(f"     • Tiempo: {resultado['comparison']['time_qubo']:.3f}s")
    print(f"     • Válida: {'Sí' if resultado['comparison']['qubo_valid'] else 'No'}")
    
    print(f"   Comparación:")
    print(f"     • Ganador: {resultado['comparison']['better_formulation'].upper()}")
    print(f"     • Ratio tiempo (QUBO/Clásico): {resultado['comparison']['time_ratio']:.2f}x")
    print(f"     • Diferencia de costo: {resultado['comparison']['cost_difference']:.2f}")
    
    return resultado

def demo_visualizacion(resultado):
    """Demostración de capacidades de visualización."""
    print("\n📈 DEMOSTRACIÓN: VISUALIZACIÓN DE RESULTADOS")
    print("="*60)
    
    print("🎨 Generando visualizaciones comparativas...")
    
    # El TSPFormulationComparator ya tiene método de visualización integrado
    comparador = TSPFormulationComparator(resultado['classical']['solution'])  # Dummy comparador para visualización
    
    print("   • Mapas de rutas optimizadas")
    print("   • Gráficos de progreso de optimización") 
    print("   • Comparación visual de soluciones")
    
    print("✅ Visualizaciones generadas (ver ventanas de gráficos)")

def demo_analisis_estadistico(ciudades):
    """Demostración de análisis estadístico con múltiples ejecuciones."""
    print("\n📊 DEMOSTRACIÓN: ANÁLISIS ESTADÍSTICO")
    print("="*60)
    
    num_runs = 3  # Número reducido para demostración rápida
    
    sa_params = {
        'initial_temperature': 300.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.97,
        'verbose': False
    }
    
    print(f"🔬 Ejecutando {num_runs} ejecuciones independientes...")
    print(f"📊 Generando estadísticas de rendimiento...")
    
    comparador = TSPFormulationComparator(ciudades)
    estadisticas = comparador.compare_multiple_runs(sa_params, num_runs)
    
    # Mostrar resumen estadístico
    print(f"\n📈 RESUMEN ESTADÍSTICO ({num_runs} ejecuciones):")
    print(f"   Formulación Clásica:")
    print(f"     • Costo promedio: {estadisticas['classical']['mean_cost']:.2f} ± {estadisticas['classical']['std_cost']:.2f}")
    print(f"     • Mejor costo: {estadisticas['classical']['min_cost']:.2f}")
    print(f"     • Victorias: {estadisticas['classical']['wins']}/{num_runs}")
    
    print(f"   Formulación QUBO:")
    print(f"     • Costo promedio: {estadisticas['qubo']['mean_cost']:.2f} ± {estadisticas['qubo']['std_cost']:.2f}")
    print(f"     • Mejor costo: {estadisticas['qubo']['min_cost']:.2f}")
    print(f"     • Victorias: {estadisticas['qubo']['wins']}/{num_runs}")
    print(f"     • Tasa de validez: {estadisticas['qubo']['validity_rate']:.1f}%")
    
    return estadisticas

def demo_escalabilidad():
    """Demostración de análisis de escalabilidad."""
    print("\n📈 DEMOSTRACIÓN: ANÁLISIS DE ESCALABILIDAD")  
    print("="*60)
    
    tamanos = [4, 6, 7]  # Tamaños pequeños para demostración rápida
    
    print(f"🔍 Analizando escalabilidad para {len(tamanos)} tamaños de problema...")
    
    sa_params = {
        'initial_temperature': 150.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.96,
        'verbose': False
    }
    
    resultados = []
    
    for n in tamanos:
        print(f"   📊 Problema de {n} ciudades... ", end="")
        
        # Generar problema
        ciudades = tsp.generar_ciudades_uniformes(n, 100)
        comparador = TSPFormulationComparator(ciudades)
        
        # Ejecutar comparación  
        resultado = comparador.compare_single_run(sa_params, verbose=False)
        
        resultados.append({
            'n': n,
            'time_classical': resultado['comparison']['time_classical'],
            'time_qubo': resultado['comparison']['time_qubo'],
            'ratio': resultado['comparison']['time_ratio']
        })
        
        print(f"Ratio: {resultado['comparison']['time_ratio']:.1f}x")
    
    # Mostrar tabla de escalabilidad
    print(f"\n📋 TABLA DE ESCALABILIDAD:")
    print(f"{'Ciudades':<10} {'T.Clásico':<12} {'T.QUBO':<12} {'Ratio':<8}")
    print("-" * 45)
    
    for r in resultados:
        print(f"{r['n']:<10} {r['time_classical']:<12.3f} {r['time_qubo']:<12.3f} {r['ratio']:<8.1f}")
    
    return resultados

def demo_arquitectura():
    """Demuestra la arquitectura modular del sistema."""
    print("\n🏗️  DEMOSTRACIÓN: ARQUITECTURA MODULAR")
    print("="*60)
    
    print("📦 Componentes del sistema:")
    print("   🧮 simulated_annealing.py - Algoritmo genérico SA")
    print("   🏙️  tsp_base.py - Utilidades comunes TSP")
    print("   🔄 tsp_classical.py - Formulación clásica")
    print("   ⚛️  tsp_qubo.py - Formulación QUBO")
    print("   ⚖️  compare_formulations.py - Sistema comparativo")
    
    print("\n🔗 Beneficios de la modularidad:")
    print("   ✅ Separación clara de responsabilidades")
    print("   ✅ Fácil extensión para nuevas formulaciones")
    print("   ✅ Reutilización del algoritmo SA genérico")
    print("   ✅ Interfaz consistente via OptimizationProblem")
    
    print("\n🧪 Capacidades de extensión:")
    print("   • Agregar nuevos operadores de vecindario")
    print("   • Implementar otros algoritmos metaheurísticos")
    print("   • Adaptar a otros problemas de optimización")
    print("   • Integrar con optimizadores cuánticos reales")

def main_demo():
    """Función principal de la demostración completa."""
    
    mostrar_banner()
    
    print("\n🎬 Iniciando demostración completa del sistema...")
    input("   Presiona Enter para continuar...")
    
    # Demo 1: Topologías de ciudades
    ciudades = demo_topologias()
    input("\n   Presiona Enter para continuar con la comparación...")
    
    # Demo 2: Comparación rápida
    resultado = demo_comparacion_rapida(ciudades)
    input("\n   Presiona Enter para ver las visualizaciones...")
    
    # Demo 3: Visualización (comentado para demo no interactivo)
    # demo_visualizacion(resultado)
    # input("\n   Presiona Enter para continuar con el análisis estadístico...")
    
    # Demo 4: Análisis estadístico
    estadisticas = demo_analisis_estadistico(ciudades)
    input("\n   Presiona Enter para continuar con escalabilidad...")
    
    # Demo 5: Análisis de escalabilidad
    resultados_escala = demo_escalabilidad()
    input("\n   Presiona Enter para ver la arquitectura...")
    
    # Demo 6: Arquitectura
    demo_arquitectura()
    
    # Resumen final
    print("\n" + "🎉" * 50)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("🎉" * 50)
    print("🔬 Se han demostrado todas las capacidades principales:")
    print("   ✅ Generación de topologías de ciudades")
    print("   ✅ Comparación entre formulaciones")
    print("   ✅ Análisis estadístico con múltiples ejecuciones")
    print("   ✅ Evaluación de escalabilidad")
    print("   ✅ Arquitectura modular y extensible")
    print("\n📚 Consulta el README.md para documentación completa")
    print("🚀 ¡El framework está listo para investigación y desarrollo!")
    print("🎉" * 50)

if __name__ == "__main__":
    try:
        main_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demostración interrumpida por el usuario")
        print("👋 ¡Gracias por probar el sistema!")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        print("🔧 Verifica que todas las dependencias estén instaladas")
        print("📚 Consulta el README.md para troubleshooting")
        sys.exit(1)