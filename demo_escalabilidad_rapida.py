#!/usr/bin/env python3
"""
📈 Demo Rápida de Escalabilidad TSP: 10-150 ciudades

Ejecuta análisis automático de escalabilidad y genera gráficas comparativas.
Versión optimizada sin interacción del usuario.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

def demo_escalabilidad_rapida():
    """Demo rápida de escalabilidad con parámetros preconfigurados."""
    
    print("📈" * 60)
    print("🚀 DEMO RÁPIDA: ESCALABILIDAD TSP CLÁSICO vs QUBO")
    print("📈" * 60)
    print("🎯 Rango: 10-150 ciudades (intervalos de 10)")
    print("📊 Topología: Ciudades uniformes")
    print("⚡ Parámetros SA optimizados para velocidad")
    print("📈" * 60)
    
    # Configuración optimizada para demo rápida
    rangos = list(range(10, 151, 10))  # 10, 20, 30, ..., 150
    
    # Parámetros SA más rápidos
    sa_params = {
        'initial_temperature': 300.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.95,  # Enfriamiento más rápido
        'verbose': False
    }
    
    # Almacenar resultados
    resultados = {
        'ciudades': [],
        'costo_clasico': [],
        'costo_qubo': [],
        'tiempo_clasico': [],
        'tiempo_qubo': [],
        'qubo_valido': []
    }
    
    print(f"\n🔬 Ejecutando análisis en {len(rangos)} puntos de datos...")
    start_total = time.time()
    
    for i, n in enumerate(rangos):
        print(f"📊 {n:3d} ciudades ({i+1:2d}/{len(rangos):2d}): ", end="", flush=True)
        
        try:
            # Generar ciudades uniformes
            ciudades = tsp.generar_ciudades_uniformes(n, 200)
            
            # Crear comparador
            comparador = TSPFormulationComparator(ciudades)
            
            # Ejecutar comparación
            start_iter = time.time()
            resultado = comparador.compare_single_run(sa_params, verbose=False)
            iter_time = time.time() - start_iter
            
            # Guardar resultados
            resultados['ciudades'].append(n)
            resultados['costo_clasico'].append(resultado['comparison']['tour_cost_classical'])
            resultados['costo_qubo'].append(resultado['comparison']['tour_cost_qubo'])
            resultados['tiempo_clasico'].append(resultado['comparison']['time_classical'])
            resultados['tiempo_qubo'].append(resultado['comparison']['time_qubo'])
            resultados['qubo_valido'].append(resultado['comparison']['qubo_valid'])
            
            # Mostrar progreso
            print(f"Clás={resultado['comparison']['time_classical']:.3f}s, "
                  f"QUBO={resultado['comparison']['time_qubo']:.3f}s, "
                  f"Válido={'✓' if resultado['comparison']['qubo_valid'] else '✗'} "
                  f"({iter_time:.1f}s)")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:30]}...")
            # Agregar NaN para mantener consistencia
            resultados['ciudades'].append(n)
            for key in ['costo_clasico', 'costo_qubo', 'tiempo_clasico', 'tiempo_qubo']:
                resultados[key].append(np.nan)
            resultados['qubo_valido'].append(False)
    
    total_time = time.time() - start_total
    print(f"\n⏱️  Análisis completado en {total_time/60:.1f} minutos")
    
    return resultados

def crear_graficas_comparativas(resultados):
    """Crea las gráficas comparativas solicitadas."""
    
    print("\n📊 Generando gráficas comparativas...")
    
    # Filtrar datos válidos
    datos_validos = []
    for i, n in enumerate(resultados['ciudades']):
        if not (np.isnan(resultados['costo_clasico'][i]) or np.isnan(resultados['tiempo_clasico'][i])):
            datos_validos.append(i)
    
    if len(datos_validos) < 2:
        print("❌ Datos insuficientes para generar gráficas")
        return
    
    # Extraer datos válidos
    ciudades = [resultados['ciudades'][i] for i in datos_validos]
    costo_clasico = [resultados['costo_clasico'][i] for i in datos_validos]
    costo_qubo = [resultados['costo_qubo'][i] for i in datos_validos]
    tiempo_clasico = [resultados['tiempo_clasico'][i] for i in datos_validos]
    tiempo_qubo = [resultados['tiempo_qubo'][i] for i in datos_validos]
    
    # Crear figura con 2 subgráficas principales (como solicitado)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análisis de Escalabilidad TSP: Clásico vs QUBO\n10-150 ciudades', 
                 fontsize=14, fontweight='bold')
    
    # Gráfica 1: Número de Ciudades vs Costo
    ax1.plot(ciudades, costo_clasico, 'o-', color='blue', linewidth=3, markersize=8, 
             label='Formulación Clásica', alpha=0.8)
    ax1.plot(ciudades, costo_qubo, 's-', color='red', linewidth=3, markersize=8, 
             label='Formulación QUBO', alpha=0.8)
    ax1.set_xlabel('Número de Ciudades', fontsize=12)
    ax1.set_ylabel('Costo del Tour', fontsize=12)
    ax1.set_title('Costo vs Número de Ciudades', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    
    # Gráfica 2: Número de Ciudades vs Tiempo
    ax2.plot(ciudades, tiempo_clasico, 'o-', color='blue', linewidth=3, markersize=8, 
             label='Formulación Clásica', alpha=0.8)
    ax2.plot(ciudades, tiempo_qubo, 's-', color='red', linewidth=3, markersize=8, 
             label='Formulación QUBO', alpha=0.8)
    ax2.set_xlabel('Número de Ciudades', fontsize=12)
    ax2.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
    ax2.set_title('Tiempo vs Número de Ciudades', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    ax2.set_yscale('log')  # Escala logarítmica para mejor visualización
    
    plt.tight_layout()
    
    # Guardar gráfica
    nombre_archivo = 'escalabilidad_tsp_10_150_ciudades.png'
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"📁 Gráficas guardadas como: {nombre_archivo}")
    
    # Mostrar gráficas
    plt.show()
    
    # Crear gráfica adicional con análisis de ratios
    crear_grafica_ratios(ciudades, tiempo_clasico, tiempo_qubo, costo_clasico, costo_qubo)

def crear_grafica_ratios(ciudades, tiempo_clasico, tiempo_qubo, costo_clasico, costo_qubo):
    """Crea gráfica adicional de análisis de ratios."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análisis Comparativo Detallado: Ratios QUBO/Clásico', 
                 fontsize=14, fontweight='bold')
    
    # Calcular ratios
    ratios_tiempo = [t_q/t_c if t_c > 0 else np.nan for t_q, t_c in zip(tiempo_qubo, tiempo_clasico)]
    ratios_costo = [c_q/c_c if c_c > 0 else np.nan for c_q, c_c in zip(costo_qubo, costo_clasico)]
    
    # Gráfica 1: Ratio de Tiempos
    ax1.plot(ciudades, ratios_tiempo, 'o-', color='orange', linewidth=3, markersize=8)
    ax1.set_xlabel('Número de Ciudades', fontsize=12)
    ax1.set_ylabel('Ratio de Tiempo (QUBO/Clásico)', fontsize=12)
    ax1.set_title('Sobrecarga Temporal de QUBO', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=1, color='black', linestyle='--', alpha=0.7, label='Rendimiento igual')
    ax1.legend()
    ax1.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    
    # Gráfica 2: Ratio de Costos
    ax2.plot(ciudades, ratios_costo, 'o-', color='green', linewidth=3, markersize=8)
    ax2.set_xlabel('Número de Ciudades', fontsize=12)
    ax2.set_ylabel('Ratio de Costo (QUBO/Clásico)', fontsize=12)
    ax2.set_title('Calidad Relativa de QUBO', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=1, color='black', linestyle='--', alpha=0.7, label='Calidad igual')
    ax2.legend()
    ax2.set_xlim(min(ciudades) - 5, max(ciudades) + 5)
    
    plt.tight_layout()
    
    # Guardar
    plt.savefig('ratios_tsp_10_150_ciudades.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("📁 Análisis de ratios guardado como: ratios_tsp_10_150_ciudades.png")

def mostrar_estadisticas_finales(resultados):
    """Muestra estadísticas resumidas del análisis."""
    
    print("\n📊 ESTADÍSTICAS FINALES")
    print("=" * 50)
    
    # Filtrar datos válidos
    datos_validos = []
    for i, n in enumerate(resultados['ciudades']):
        if not np.isnan(resultados['tiempo_clasico'][i]):
            datos_validos.append(i)
    
    if not datos_validos:
        print("❌ No hay datos válidos")
        return
    
    ciudades = [resultados['ciudades'][i] for i in datos_validos]
    tiempos_clasico = [resultados['tiempo_clasico'][i] for i in datos_validos]
    tiempos_qubo = [resultados['tiempo_qubo'][i] for i in datos_validos]
    costos_clasico = [resultados['costo_clasico'][i] for i in datos_validos]
    costos_qubo = [resultados['costo_qubo'][i] for i in datos_validos]
    validez = [resultados['qubo_valido'][i] for i in datos_validos]
    
    print(f"🎯 Rango analizado: {min(ciudades)} - {max(ciudades)} ciudades")
    print(f"📊 Puntos exitosos: {len(datos_validos)}/{len(resultados['ciudades'])}")
    
    print(f"\n⏱️  RENDIMIENTO TEMPORAL:")
    print(f"   Clásico: {min(tiempos_clasico):.3f}s - {max(tiempos_clasico):.3f}s (promedio: {np.mean(tiempos_clasico):.3f}s)")
    print(f"   QUBO:    {min(tiempos_qubo):.3f}s - {max(tiempos_qubo):.3f}s (promedio: {np.mean(tiempos_qubo):.3f}s)")
    
    ratios_tiempo = [t_q/t_c for t_q, t_c in zip(tiempos_qubo, tiempos_clasico) if t_c > 0]
    print(f"   Ratio promedio (QUBO/Clásico): {np.mean(ratios_tiempo):.2f}x")
    
    print(f"\n💰 CALIDAD DE SOLUCIONES:")
    print(f"   Clásico: {min(costos_clasico):.1f} - {max(costos_clasico):.1f} (promedio: {np.mean(costos_clasico):.1f})")
    print(f"   QUBO:    {min(costos_qubo):.1f} - {max(costos_qubo):.1f} (promedio: {np.mean(costos_qubo):.1f})")
    
    print(f"\n✅ VALIDEZ QUBO: {sum(validez)}/{len(validez)} ({sum(validez)/len(validez)*100:.1f}%)")
    
    # Conclusiones
    print(f"\n🔍 CONCLUSIONES:")
    ratio_prom = np.mean(ratios_tiempo)
    if ratio_prom < 2:
        print("   • QUBO muestra overhead temporal moderado")
    elif ratio_prom < 5:
        print("   • QUBO tiene overhead temporal considerable pero manejable")
    else:
        print("   • QUBO muestra overhead temporal significativo")
    
    tasa_validez = sum(validez)/len(validez)*100
    if tasa_validez >= 95:
        print("   • Excelente tasa de validez en soluciones QUBO")
    elif tasa_validez >= 80:
        print("   • Buena tasa de validez en soluciones QUBO")
    else:
        print("   • Tasa de validez QUBO requiere atención")

def main():
    """Función principal de la demo de escalabilidad."""
    
    print("🚀 Iniciando demo de escalabilidad TSP...")
    
    # Ejecutar análisis
    resultados = demo_escalabilidad_rapida()
    
    # Crear gráficas
    crear_graficas_comparativas(resultados)
    
    # Mostrar estadísticas
    mostrar_estadisticas_finales(resultados)
    
    print("\n🎉 DEMO DE ESCALABILIDAD COMPLETADA")
    print("="*50)
    print("📊 Se generaron las gráficas solicitadas:")
    print("   ✅ Número de ciudades vs Costo (ambas formulaciones)")
    print("   ✅ Número de ciudades vs Tiempo (ambas formulaciones)")
    print("   ✅ Análisis adicional de ratios comparativos")
    print("\n📁 Archivos generados:")
    print("   • escalabilidad_tsp_10_150_ciudades.png")
    print("   • ratios_tsp_10_150_ciudades.png")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()