"""
Comparación de formulaciones del TSP: Clásica vs QUBO

Este script compara el rendimiento del algoritmo Simulated Annealing aplicado 
a dos formulaciones diferentes del problema del Viajante de Comercio:
1. Formulación Clásica: permutaciones de ciudades
2. Formulación QUBO: matriz binaria de asignación

Autor: Sistema de Optimización Cuántica
Fecha: Octubre 2025
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Any

from simulated_annealing import SimulatedAnnealing, plot_optimization_progress
from tsp_classical import TSPClassical
from tsp_qubo import TSPQUBO
import tsp_base as tsp


class TSPFormulationComparator:
    """
    Clase para comparar diferentes formulaciones del TSP.
    """
    
    def __init__(self, ciudades: Dict[str, Tuple[int, int]]):
        """
        Inicializa el comparador con un conjunto de ciudades.
        
        Args:
            ciudades: Diccionario {nombre_ciudad: (x, y)}
        """
        self.ciudades = ciudades
        self.n = len(ciudades)
        
        # Crear instancias de los problemas
        self.tsp_classical = TSPClassical(ciudades, operacion_vecindario="2opt")
        self.tsp_qubo = TSPQUBO(ciudades, penalty_factor=1000.0)
        
        # Resultados de comparación
        self.results = {}
    
    def compare_single_run(self, sa_params: Dict, verbose: bool = True) -> Dict:
        """
        Compara una ejecución única de ambas formulaciones.
        
        Args:
            sa_params: Parámetros para Simulated Annealing
            verbose: Si mostrar información detallada
            
        Returns:
            Diccionario con resultados de la comparación
        """
        if verbose:
            print("="*80)
            print(f"COMPARACIÓN TSP: CLÁSICO vs QUBO ({self.n} ciudades)")
            print("="*80)
        
        results = {
            'classical': {},
            'qubo': {},
            'comparison': {}
        }
        
        # === FORMULACIÓN CLÁSICA ===
        if verbose:
            print("\n--- FORMULACIÓN CLÁSICA ---")
        
        start_time = time.time()
        
        # Crear optimizador clásico
        sa_params_classical = sa_params.copy()
        sa_params_classical['verbose'] = verbose
        sa_classical = SimulatedAnnealing(self.tsp_classical, **sa_params_classical)
        
        # Ejecutar optimización
        best_solution_classical, best_cost_classical, stats_classical = sa_classical.optimize()
        
        classical_time = time.time() - start_time
        
        # Obtener información de la solución
        info_classical = self.tsp_classical.get_solution_info(best_solution_classical)
        
        results['classical'] = {
            'solution': best_solution_classical,
            'cost': best_cost_classical,
            'info': info_classical,
            'statistics': stats_classical,
            'execution_time': classical_time
        }
        
        if verbose:
            print(f"Tiempo de ejecución: {classical_time:.2f} segundos")
            print(f"Costo final: {best_cost_classical:.2f}")
            print(f"Mejora: {stats_classical['improvement']:.2f}%")
        
        # === FORMULACIÓN QUBO ===
        if verbose:
            print("\n--- FORMULACIÓN QUBO ---")
        
        start_time = time.time()
        
        # Crear optimizador QUBO
        sa_params_qubo = sa_params.copy()
        sa_params_qubo['verbose'] = verbose
        sa_qubo = SimulatedAnnealing(self.tsp_qubo, **sa_params_qubo)
        
        # Ejecutar optimización
        best_solution_qubo, best_cost_qubo, stats_qubo = sa_qubo.optimize()
        
        qubo_time = time.time() - start_time
        
        # Obtener información de la solución QUBO
        info_qubo = self.tsp_qubo.get_solution_info(best_solution_qubo)
        
        results['qubo'] = {
            'solution': best_solution_qubo,
            'cost': best_cost_qubo,
            'info': info_qubo,
            'statistics': stats_qubo,
            'execution_time': qubo_time
        }
        
        if verbose:
            print(f"Tiempo de ejecución: {qubo_time:.2f} segundos")
            print(f"Costo QUBO: {best_cost_qubo:.2f}")
            print(f"Costo del tour: {info_qubo['tour_cost']:.2f}")
            print(f"Solución válida: {info_qubo['is_valid']}")
            print(f"Violaciones: {info_qubo['violations']}")
            print(f"Mejora: {stats_qubo['improvement']:.2f}%")
        
        # === COMPARACIÓN ===
        # Comparar costos de tour (la métrica real del TSP)
        tour_cost_classical = best_cost_classical
        tour_cost_qubo = info_qubo['tour_cost'] if info_qubo['is_valid'] else float('inf')
        
        # Métricas de comparación
        time_ratio = qubo_time / classical_time if classical_time > 0 else float('inf')
        cost_difference = tour_cost_qubo - tour_cost_classical
        cost_ratio = tour_cost_qubo / tour_cost_classical if tour_cost_classical > 0 else float('inf')
        
        results['comparison'] = {
            'tour_cost_classical': tour_cost_classical,
            'tour_cost_qubo': tour_cost_qubo,
            'cost_difference': cost_difference,
            'cost_ratio': cost_ratio,
            'time_classical': classical_time,
            'time_qubo': qubo_time,
            'time_ratio': time_ratio,
            'qubo_valid': info_qubo['is_valid'],
            'better_formulation': 'classical' if tour_cost_classical < tour_cost_qubo else 'qubo'
        }
        
        if verbose:
            print("\n--- RESUMEN COMPARATIVO ---")
            print(f"Costo tour clásico: {tour_cost_classical:.2f}")
            print(f"Costo tour QUBO: {tour_cost_qubo:.2f}")
            print(f"Diferencia de costo: {cost_difference:.2f}")
            print(f"Ratio de costo (QUBO/Clásico): {cost_ratio:.3f}")
            print(f"Ratio de tiempo (QUBO/Clásico): {time_ratio:.3f}")
            print(f"Mejor formulación: {results['comparison']['better_formulation'].upper()}")
            print(f"QUBO válido: {info_qubo['is_valid']}")
        
        return results
    
    def compare_multiple_runs(self, sa_params: Dict, num_runs: int = 5) -> Dict:
        """
        Compara múltiples ejecuciones para análisis estadístico.
        
        Args:
            sa_params: Parámetros para Simulated Annealing
            num_runs: Número de ejecuciones independientes
            
        Returns:
            Diccionario con estadísticas de comparación
        """
        print(f"\n{'='*80}")
        print(f"COMPARACIÓN ESTADÍSTICA: {num_runs} EJECUCIONES")
        print(f"{'='*80}")
        
        # Almacenar resultados de múltiples ejecuciones
        classical_costs = []
        qubo_costs = []
        classical_times = []
        qubo_times = []
        qubo_valid_count = 0
        
        classical_wins = 0
        qubo_wins = 0
        
        for run in range(num_runs):
            print(f"\n--- Ejecución {run + 1}/{num_runs} ---")
            
            result = self.compare_single_run(sa_params, verbose=False)
            
            classical_costs.append(result['comparison']['tour_cost_classical'])
            qubo_costs.append(result['comparison']['tour_cost_qubo'])
            classical_times.append(result['comparison']['time_classical'])
            qubo_times.append(result['comparison']['time_qubo'])
            
            if result['comparison']['qubo_valid']:
                qubo_valid_count += 1
                
                if result['comparison']['better_formulation'] == 'classical':
                    classical_wins += 1
                else:
                    qubo_wins += 1
            else:
                classical_wins += 1  # Si QUBO es inválido, clásico gana
            
            print(f"Clásico: {result['comparison']['tour_cost_classical']:.2f}, "
                  f"QUBO: {result['comparison']['tour_cost_qubo']:.2f}, "
                  f"Mejor: {result['comparison']['better_formulation']}")
        
        # Calcular estadísticas
        stats = {
            'num_runs': num_runs,
            'classical': {
                'costs': classical_costs,
                'mean_cost': np.mean(classical_costs),
                'std_cost': np.std(classical_costs),
                'min_cost': np.min(classical_costs),
                'max_cost': np.max(classical_costs),
                'mean_time': np.mean(classical_times),
                'std_time': np.std(classical_times),
                'wins': classical_wins
            },
            'qubo': {
                'costs': qubo_costs,
                'mean_cost': np.mean(qubo_costs),
                'std_cost': np.std(qubo_costs),
                'min_cost': np.min(qubo_costs),
                'max_cost': np.max(qubo_costs),
                'mean_time': np.mean(qubo_times),
                'std_time': np.std(qubo_times),
                'wins': qubo_wins,
                'valid_solutions': qubo_valid_count,
                'validity_rate': qubo_valid_count / num_runs * 100
            }
        }
        
        # Mostrar estadísticas
        print(f"\n{'='*60}")
        print("ESTADÍSTICAS FINALES")
        print(f"{'='*60}")
        
        print("\nFormulación Clásica:")
        print(f"  Costo promedio: {stats['classical']['mean_cost']:.2f} ± {stats['classical']['std_cost']:.2f}")
        print(f"  Rango: [{stats['classical']['min_cost']:.2f}, {stats['classical']['max_cost']:.2f}]")
        print(f"  Tiempo promedio: {stats['classical']['mean_time']:.2f}s ± {stats['classical']['std_time']:.2f}s")
        print(f"  Victorias: {stats['classical']['wins']}/{num_runs}")
        
        print("\nFormulación QUBO:")
        print(f"  Costo promedio: {stats['qubo']['mean_cost']:.2f} ± {stats['qubo']['std_cost']:.2f}")
        print(f"  Rango: [{stats['qubo']['min_cost']:.2f}, {stats['qubo']['max_cost']:.2f}]")
        print(f"  Tiempo promedio: {stats['qubo']['mean_time']:.2f}s ± {stats['qubo']['std_time']:.2f}s")
        print(f"  Victorias: {stats['qubo']['wins']}/{num_runs}")
        print(f"  Soluciones válidas: {stats['qubo']['valid_solutions']}/{num_runs} ({stats['qubo']['validity_rate']:.1f}%)")
        
        return stats
    
    def visualize_comparison(self, result: Dict):
        """
        Crea visualizaciones comparativas de los resultados.
        
        Args:
            result: Resultado de compare_single_run()
        """
        # Obtener rutas para visualización
        ruta_classical = result['classical']['solution']
        
        # Convertir solución QUBO a ruta
        matriz_qubo = result['qubo']['solution']
        ruta_qubo = self.tsp_qubo.solution_to_route(matriz_qubo)
        
        if ruta_qubo is None:
            print("⚠️  La solución QUBO es inválida, no se puede visualizar la ruta")
            ruta_qubo = tsp.generar_ruta_aleatoria(self.ciudades)  # Ruta dummy para visualización
        
        # Mostrar comparación de rutas
        tsp.comparar_rutas(
            ruta_classical, ruta_qubo, 
            self.ciudades,
            etiquetas=(f"Clásico (Costo: {result['comparison']['tour_cost_classical']:.1f})",
                      f"QUBO (Costo: {result['comparison']['tour_cost_qubo']:.1f})"),
            colores=('blue', 'red')
        )
        
        # Graficar progreso de optimización
        plot_optimization_progress(result['classical']['statistics'], 
                                 "Progreso - Formulación Clásica")
        plot_optimization_progress(result['qubo']['statistics'], 
                                 "Progreso - Formulación QUBO")
    
    def visualize_statistics(self, stats: Dict):
        """
        Crea visualizaciones de las estadísticas de múltiples ejecuciones.
        
        Args:
            stats: Resultado de compare_multiple_runs()
        """
        _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Comparación de costos
        classical_costs = stats['classical']['costs']
        qubo_costs = stats['qubo']['costs']
        
        ax1.boxplot([classical_costs, qubo_costs], 
                   labels=['Clásico', 'QUBO'])
        ax1.set_ylabel('Costo del Tour')
        ax1.set_title('Distribución de Costos')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Comparación de tiempos
        x_pos = [0, 1]
        ax2.bar(x_pos, [stats['classical']['mean_time'], stats['qubo']['mean_time']], 
               color=['blue', 'red'], alpha=0.7)
        ax2.errorbar(x_pos, [stats['classical']['mean_time'], stats['qubo']['mean_time']], 
                    yerr=[stats['classical']['std_time'], stats['qubo']['std_time']],
                    fmt='none', color='black', capsize=5)
        ax2.set_ylabel('Tiempo (segundos)')
        ax2.set_title('Tiempo de Ejecución Promedio')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(['Clásico', 'QUBO'])
        ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Tasa de victoria
        ax3.pie([stats['classical']['wins'], stats['qubo']['wins']], 
               labels=[f"Clásico ({stats['classical']['wins']})", 
                      f"QUBO ({stats['qubo']['wins']})"],
               colors=['blue', 'red'], autopct='%1.1f%%')
        ax3.set_title('Tasa de Victoria por Formulación')
        
        # Gráfico 4: Validez de soluciones QUBO
        valid_count = stats['qubo']['valid_solutions']
        invalid_count = stats['num_runs'] - valid_count
        
        ax4.pie([valid_count, invalid_count], 
               labels=[f'Válidas ({valid_count})', f'Inválidas ({invalid_count})'],
               colors=['green', 'orange'], autopct='%1.1f%%')
        ax4.set_title('Validez de Soluciones QUBO')
        
        plt.tight_layout()
        plt.show()


def main_comparison():
    """
    Función principal para ejecutar la comparación de formulaciones.
    """
    print("🔬 COMPARADOR DE FORMULACIONES TSP: CLÁSICO vs QUBO")
    print("="*80)
    
    # Configuración del experimento
    num_ciudades = 8  # QUBO es más complejo, usar menos ciudades
    mapa_size = 200
    
    # Generar ciudades
    print(f"Generando {num_ciudades} ciudades...")
    ciudades = tsp.generar_ciudades_clusters(num_ciudades, mapa_size, num_clusters=3)
    
    # Mostrar mapa de ciudades
    tsp.mostrar_mapa_ciudades(ciudades, f"Ciudades para Comparación ({num_ciudades} ciudades)")
    
    # Configurar parámetros de SA
    sa_params = {
        'initial_temperature': 1000.0,
        'final_temperature': 0.1,
        'cooling_rate': 0.99,  # Enfriamiento más rápido para pruebas
        'verbose': True,
        'progress_interval': 1000
    }
    
    # Crear comparador
    comparador = TSPFormulationComparator(ciudades)
    
    # Ejecutar comparación única
    print("\n📊 EJECUTANDO COMPARACIÓN ÚNICA...")
    resultado = comparador.compare_single_run(sa_params)
    
    # Visualizar comparación
    print("\n📈 GENERANDO VISUALIZACIONES...")
    comparador.visualize_comparison(resultado)
    
    # Ejecutar comparación múltiple (opcional)
    respuesta = input("\n¿Ejecutar comparación estadística con múltiples ejecuciones? (y/n): ").lower()
    if respuesta == 'y':
        num_runs = 5
        print(f"\n📊 EJECUTANDO {num_runs} EJECUCIONES PARA ESTADÍSTICAS...")
        estadisticas = comparador.compare_multiple_runs(sa_params, num_runs)
        
        print("\n📈 GENERANDO GRÁFICOS ESTADÍSTICOS...")
        comparador.visualize_statistics(estadisticas)
    
    print("\n✅ Comparación completada!")


if __name__ == "__main__":
    main_comparison()