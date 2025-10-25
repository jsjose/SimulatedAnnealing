#!/usr/bin/env python3
"""
📈 Demo de Escalabilidad TSP Optimizada: 10-100 ciudades

Análisis de escalabilidad optimizado con rango práctico y ejecución eficiente.
Genera las gráficas solicitadas: ciudades vs costo y ciudades vs tiempo.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from compare_formulations import TSPFormulationComparator
import tsp_base as tsp

def ejecutar_analisis_optimizado():
    """Ejecuta análisis de escalabilidad optimizado para demostración."""
    
    print("🚀" * 60)
    print("📈 ANÁLISIS DE ESCALABILIDAD TSP: CLÁSICO vs QUBO")
    print("🚀" * 60)
    print("🎯 Rango optimizado: 10-100 ciudades (intervalos de 10)")
    print("⚡ Parámetros SA balanceados para calidad/velocidad")
    print("📊 Generará gráficas: Costo vs Ciudades, Tiempo vs Ciudades")
    print("🚀" * 60)
    
    # Configuración del análisis
    rangos = list(range(10, 101, 10))  # 10, 20, 30, ..., 100
    print(f"\n🔬 Analizando {len(rangos)} puntos de datos: {rangos}")
    
    # Parámetros SA adaptativos según tamaño
    def get_sa_params(n):
        if n <= 30:
            return {'initial_temperature': 300.0, 'final_temperature': 0.1, 'cooling_rate': 0.96}
        elif n <= 60:
            return {'initial_temperature': 500.0, 'final_temperature': 0.05, 'cooling_rate': 0.97}
        else:
            return {'initial_temperature': 800.0, 'final_temperature': 0.02, 'cooling_rate': 0.98}
    
    # Almacenamiento de resultados
    resultados = {
        'ciudades': [],
        'costo_clasico': [],
        'costo_qubo': [],
        'tiempo_clasico': [],
        'tiempo_qubo': [],
        'qubo_valido': [],
        'errores': 0
    }
    
    print(f"\n⏳ Iniciando análisis (tiempo estimado: ~{len(rangos)*0.3:.1f} minutos)...")
    start_total = time.time()
    
    # Procesar cada tamaño
    for i, n in enumerate(rangos):
        print(f"📊 [{i+1:2d}/{len(rangos):2d}] {n:3d} ciudades: ", end="", flush=True)
        
        try:
            # Generar problema
            ciudades = tsp.generar_ciudades_uniformes(n, 250)
            sa_params = get_sa_params(n)
            sa_params['verbose'] = False
            
            # Ejecutar comparación
            comparador = TSPFormulationComparator(ciudades)
            resultado = comparador.compare_single_run(sa_params, verbose=False)
            
            # Almacenar resultados
            resultados['ciudades'].append(n)
            resultados['costo_clasico'].append(resultado['comparison']['tour_cost_classical'])
            resultados['costo_qubo'].append(resultado['comparison']['tour_cost_qubo'])
            resultados['tiempo_clasico'].append(resultado['comparison']['time_classical'])
            resultados['tiempo_qubo'].append(resultado['comparison']['time_qubo'])
            resultados['qubo_valido'].append(resultado['comparison']['qubo_valid'])
            
            # Mostrar progreso
            ratio_tiempo = resultado['comparison']['time_ratio']
            validez = "✓" if resultado['comparison']['qubo_valid'] else "✗"
            print(f"T_clás={resultado['comparison']['time_classical']:.3f}s, "
                  f"T_qubo={resultado['comparison']['time_qubo']:.3f}s, "
                  f"Ratio={ratio_tiempo:.1f}x, Valid={validez}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:40]}...")
            resultados['errores'] += 1
            # Usar NaN para puntos fallidos
            resultados['ciudades'].append(n)
            for key in ['costo_clasico', 'costo_qubo', 'tiempo_clasico', 'tiempo_qubo']:
                resultados[key].append(np.nan)
            resultados['qubo_valido'].append(False)
    
    total_time = time.time() - start_total
    exitosos = len(rangos) - resultados['errores']
    
    print(f"\n⏱️  Análisis completado en {total_time/60:.1f} minutos")
    print(f"✅ Casos exitosos: {exitosos}/{len(rangos)}")
    
    return resultados

def crear_graficas_principales(resultados):
    """Crea las gráficas principales solicitadas por el usuario."""
    
    print(f"\n📊 GENERANDO GRÁFICAS PRINCIPALES...")
    
    # Filtrar datos válidos (excluir NaN)
    indices_validos = []
    for i in range(len(resultados['ciudades'])):
        if not (np.isnan(resultados['costo_clasico'][i]) or np.isnan(resultados['tiempo_clasico'][i])):
            indices_validos.append(i)
    
    if len(indices_validos) < 3:
        print("❌ Datos insuficientes para gráficas")
        return
    
    # Extraer datos válidos
    ciudades = [resultados['ciudades'][i] for i in indices_validos]
    costo_clasico = [resultados['costo_clasico'][i] for i in indices_validos]
    costo_qubo = [resultados['costo_qubo'][i] for i in indices_validos]
    tiempo_clasico = [resultados['tiempo_clasico'][i] for i in indices_validos]
    tiempo_qubo = [resultados['tiempo_qubo'][i] for i in indices_validos]
    
    # CREAR FIGURA CON LAS 2 GRÁFICAS SOLICITADAS
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análisis de Escalabilidad TSP: Formulación Clásica vs QUBO\n'
                 f'Rango: {min(ciudades)}-{max(ciudades)} ciudades', 
                 fontsize=16, fontweight='bold')
    
    # GRÁFICA 1: NÚMERO DE CIUDADES vs COSTO
    ax1.plot(ciudades, costo_clasico, 'o-', color='#2E86AB', linewidth=3, markersize=8, 
             label='Formulación Clásica', alpha=0.9)
    ax1.plot(ciudades, costo_qubo, 's-', color='#A23B72', linewidth=3, markersize=8, 
             label='Formulación QUBO', alpha=0.9)
    
    ax1.set_xlabel('Número de Ciudades', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Costo del Tour', fontsize=12, fontweight='bold')
    ax1.set_title('Costo vs Número de Ciudades', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(min(ciudades) - 2, max(ciudades) + 2)
    
    # Agregar anotaciones en puntos clave
    mid_idx = len(ciudades) // 2
    ax1.annotate(f'Clásico: {costo_clasico[mid_idx]:.0f}', 
                xy=(ciudades[mid_idx], costo_clasico[mid_idx]), 
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                fontsize=9)
    ax1.annotate(f'QUBO: {costo_qubo[mid_idx]:.0f}', 
                xy=(ciudades[mid_idx], costo_qubo[mid_idx]), 
                xytext=(10, -20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightpink', alpha=0.7),
                fontsize=9)
    
    # GRÁFICA 2: NÚMERO DE CIUDADES vs TIEMPO
    ax2.plot(ciudades, tiempo_clasico, 'o-', color='#2E86AB', linewidth=3, markersize=8, 
             label='Formulación Clásica', alpha=0.9)
    ax2.plot(ciudades, tiempo_qubo, 's-', color='#A23B72', linewidth=3, markersize=8, 
             label='Formulación QUBO', alpha=0.9)
    
    ax2.set_xlabel('Número de Ciudades', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=12, fontweight='bold')
    ax2.set_title('Tiempo vs Número de Ciudades', fontsize=14, fontweight='bold', pad=20)
    ax2.legend(fontsize=11, framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(min(ciudades) - 2, max(ciudades) + 2)
    ax2.set_yscale('log')  # Escala logarítmica para mejor visualización
    
    # Agregar línea de tendencia visual
    ax2.axhline(y=1, color='gray', linestyle=':', alpha=0.5, label='1 segundo')
    
    plt.tight_layout()
    
    # Guardar gráfica principal
    filename_main = 'escalabilidad_tsp_costo_tiempo_vs_ciudades.png'
    plt.savefig(filename_main, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"📁 Gráficas principales guardadas: {filename_main}")
    
    # Mostrar gráficas
    plt.show()
    
    # Crear gráfica adicional de análisis
    crear_grafica_analisis_detallado(ciudades, tiempo_clasico, tiempo_qubo, costo_clasico, costo_qubo)
    
    return filename_main

def crear_grafica_analisis_detallado(ciudades, tiempo_clasico, tiempo_qubo, costo_clasico, costo_qubo):
    """Crea gráfica adicional con análisis detallado."""
    
    # Calcular métricas derivadas
    ratios_tiempo = [t_q/t_c if t_c > 0 else np.nan for t_q, t_c in zip(tiempo_qubo, tiempo_clasico)]
    diferencia_costo_pct = [(c_q-c_c)/c_c*100 if c_c > 0 else np.nan for c_q, c_c in zip(costo_qubo, costo_clasico)]
    
    # Crear figura de análisis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análisis Detallado: Rendimiento Relativo QUBO vs Clásico', 
                 fontsize=16, fontweight='bold')
    
    # Ratio de tiempos
    ax1.plot(ciudades, ratios_tiempo, 'o-', color='#F18F01', linewidth=3, markersize=8)
    ax1.set_xlabel('Número de Ciudades', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Ratio de Tiempo (QUBO/Clásico)', fontsize=12, fontweight='bold')
    ax1.set_title('Factor de Sobrecarga Temporal QUBO', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Rendimiento igual')
    ax1.legend()
    
    # Diferencia de costos
    ax2.plot(ciudades, diferencia_costo_pct, 'o-', color='#C73E1D', linewidth=3, markersize=8)
    ax2.set_xlabel('Número de Ciudades', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Diferencia de Costo (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Diferencia Relativa de Calidad', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='green', linestyle='--', alpha=0.7, label='Calidad igual')
    ax2.legend()
    
    plt.tight_layout()
    
    # Guardar
    filename_analysis = 'escalabilidad_tsp_analisis_detallado.png'
    plt.savefig(filename_analysis, dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print(f"📁 Análisis detallado guardado: {filename_analysis}")

def mostrar_resumen_ejecutivo(resultados):
    """Muestra resumen ejecutivo de los resultados."""
    
    print(f"\n📊 RESUMEN EJECUTIVO")
    print("=" * 60)
    
    # Filtrar datos válidos
    datos_validos = [i for i, c in enumerate(resultados['costo_clasico']) if not np.isnan(c)]
    
    if not datos_validos:
        print("❌ No hay datos válidos para el resumen")
        return
    
    ciudades = [resultados['ciudades'][i] for i in datos_validos]
    tiempos_clasico = [resultados['tiempo_clasico'][i] for i in datos_validos]
    tiempos_qubo = [resultados['tiempo_qubo'][i] for i in datos_validos]
    costos_clasico = [resultados['costo_clasico'][i] for i in datos_validos]
    costos_qubo = [resultados['costo_qubo'][i] for i in datos_validos]
    validez_qubo = [resultados['qubo_valido'][i] for i in datos_validos]
    
    # Estadísticas clave
    ratio_tiempo_prom = np.mean([t_q/t_c for t_q, t_c in zip(tiempos_qubo, tiempos_clasico)])
    tasa_validez = sum(validez_qubo) / len(validez_qubo) * 100
    
    print(f"🎯 COBERTURA DEL ANÁLISIS:")
    print(f"   • Rango de ciudades: {min(ciudades)} - {max(ciudades)}")
    print(f"   • Casos analizados: {len(datos_validos)}")
    print(f"   • Tasa de éxito: {len(datos_validos)/(len(datos_validos)+resultados['errores'])*100:.1f}%")
    
    print(f"\n⚡ RENDIMIENTO COMPUTACIONAL:")
    print(f"   • Tiempo clásico: {min(tiempos_clasico):.3f}s - {max(tiempos_clasico):.3f}s")
    print(f"   • Tiempo QUBO: {min(tiempos_qubo):.3f}s - {max(tiempos_qubo):.3f}s")
    print(f"   • Factor de sobrecarga QUBO: {ratio_tiempo_prom:.2f}x en promedio")
    
    print(f"\n🎯 CALIDAD DE SOLUCIONES:")
    diff_costo_prom = np.mean([(c_q-c_c)/c_c*100 for c_q, c_c in zip(costos_qubo, costos_clasico)])
    print(f"   • Diferencia promedio de costo: {diff_costo_prom:+.1f}%")
    print(f"   • Tasa de validez QUBO: {tasa_validez:.1f}%")
    
    print(f"\n🔍 CONCLUSIONES:")
    if ratio_tiempo_prom <= 3:
        print("   ✅ QUBO muestra overhead temporal aceptable")
    elif ratio_tiempo_prom <= 10:
        print("   ⚠️  QUBO tiene overhead temporal moderado")
    else:
        print("   ❌ QUBO muestra overhead temporal significativo")
    
    if abs(diff_costo_prom) <= 5:
        print("   ✅ Calidad de soluciones QUBO comparable al clásico")
    else:
        print("   ⚠️  Diferencia apreciable en calidad de soluciones")
    
    if tasa_validez >= 95:
        print("   ✅ Excelente tasa de validez en formulación QUBO")
    elif tasa_validez >= 85:
        print("   ⚠️  Tasa de validez QUBO aceptable")
    else:
        print("   ❌ Problemas de validez en formulación QUBO")

def main():
    """Función principal de la demo de escalabilidad."""
    
    # Ejecutar análisis
    print("🚀 Iniciando análisis de escalabilidad TSP...")
    resultados = ejecutar_analisis_optimizado()
    
    # Generar gráficas principales (las solicitadas por el usuario)
    archivo_principal = crear_graficas_principales(resultados)
    
    # Mostrar resumen
    mostrar_resumen_ejecutivo(resultados)
    
    # Mensaje final
    print(f"\n🎉 ANÁLISIS DE ESCALABILIDAD COMPLETADO")
    print("=" * 60)
    print("📊 GRÁFICAS GENERADAS (como solicitado):")
    print("   ✅ Número de ciudades vs Costo (Clásico y QUBO)")
    print("   ✅ Número de ciudades vs Tiempo (Clásico y QUBO)")
    print(f"\n📁 ARCHIVOS CREADOS:")
    print(f"   • {archivo_principal}")
    print("   • escalabilidad_tsp_analisis_detallado.png")
    print(f"\n💡 Los resultados muestran cómo escalan ambas formulaciones")
    print("   en términos de costo de solución y tiempo computacional.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Análisis interrumpido. Datos parciales pueden estar disponibles.")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()