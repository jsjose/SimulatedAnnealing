"""
Librería genérica de Simulated Annealing

Esta implementación es independiente del problema específico y puede usarse
para cualquier problema de optimización que implemente la interfaz requerida.

Autor: Sistema de Optimización Cuántica
Fecha: Octubre 2025
"""

import random
import math
from abc import ABC, abstractmethod
from typing import Any, Tuple, List, Dict, Optional


class OptimizationProblem(ABC):
    """
    Interfaz abstracta para problemas de optimización compatible con Simulated Annealing.
    
    Cualquier problema que implemente esta interfaz puede usar el algoritmo SA.
    """
    
    @abstractmethod
    def generate_initial_solution(self) -> Any:
        """
        Genera una solución inicial válida para el problema.
        
        Returns:
            Solución inicial (puede ser cualquier tipo de dato)
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, solution: Any) -> float:
        """
        Calcula el costo/energía de una solución.
        
        Args:
            solution: La solución a evaluar
            
        Returns:
            Costo de la solución (menor es mejor)
        """
        pass
    
    @abstractmethod
    def generate_neighbor(self, solution: Any) -> Any:
        """
        Genera una solución vecina a partir de la solución actual.
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución vecina
        """
        pass
    
    @abstractmethod
    def copy_solution(self, solution: Any) -> Any:
        """
        Crea una copia profunda de la solución.
        
        Args:
            solution: Solución a copiar
            
        Returns:
            Copia independiente de la solución
        """
        pass


class SimulatedAnnealing:
    """
    Implementación genérica del algoritmo Simulated Annealing.
    
    Funciona con cualquier problema que implemente la interfaz OptimizationProblem.
    """
    
    def __init__(self, problem: OptimizationProblem, 
                 initial_temperature: float = 1000.0,
                 final_temperature: float = 0.1,
                 cooling_rate: float = 0.995,
                 max_iterations: Optional[int] = None,
                 verbose: bool = True,
                 progress_interval: int = 5000):
        """
        Inicializa el algoritmo Simulated Annealing.
        
        Args:
            problem: Problema a optimizar (debe implementar OptimizationProblem)
            initial_temperature: Temperatura inicial
            final_temperature: Temperatura final
            cooling_rate: Tasa de enfriamiento (0 < rate < 1)
            max_iterations: Máximo número de iteraciones (None = hasta T_final)
            verbose: Si mostrar progreso durante la ejecución
            progress_interval: Intervalo para mostrar progreso
        """
        self.problem = problem
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.progress_interval = progress_interval
        
        # Estadísticas de ejecución
        self.reset_statistics()
    
    def reset_statistics(self):
        """Reinicia las estadísticas de ejecución."""
        self.iterations = 0
        self.accepted_moves = 0
        self.rejected_moves = 0
        self.temperature_history = []
        self.cost_history = []
        self.best_cost_history = []
    
    def acceptance_probability(self, current_cost: float, new_cost: float, 
                             temperature: float) -> float:
        """
        Calcula la probabilidad de aceptar una solución peor.
        
        Args:
            current_cost: Costo de la solución actual
            new_cost: Costo de la nueva solución
            temperature: Temperatura actual
            
        Returns:
            Probabilidad de aceptación (0 <= p <= 1)
        """
        if new_cost < current_cost:
            return 1.0  # Siempre acepta mejores soluciones
        
        if temperature <= 0:
            return 0.0  # No acepta soluciones peores a temperatura 0
        
        delta_cost = new_cost - current_cost
        return math.exp(-delta_cost / temperature)
    
    def should_terminate(self, temperature: float, iteration: int) -> bool:
        """
        Determina si el algoritmo debe terminar.
        
        Args:
            temperature: Temperatura actual
            iteration: Iteración actual
            
        Returns:
            True si debe terminar
        """
        # Terminar si la temperatura es muy baja
        if temperature <= self.final_temperature:
            return True
        
        # Terminar si se alcanza el máximo de iteraciones
        if self.max_iterations and iteration >= self.max_iterations:
            return True
        
        return False
    
    def optimize(self) -> Tuple[Any, float, Dict]:
        """
        Ejecuta el algoritmo de Simulated Annealing.
        
        Returns:
            Tupla con (mejor_solución, mejor_costo, estadísticas)
        """
        if self.verbose:
            print(f"Iniciando Simulated Annealing...")
            print(f"Temperatura inicial: {self.initial_temperature}")
            print(f"Temperatura final: {self.final_temperature}")
            print(f"Tasa de enfriamiento: {self.cooling_rate}")
            print("-" * 50)
        
        # Reiniciar estadísticas
        self.reset_statistics()
        
        # Inicializar
        temperature = self.initial_temperature
        current_solution = self.problem.generate_initial_solution()
        current_cost = self.problem.calculate_cost(current_solution)
        
        # Mejor solución global
        best_solution = self.problem.copy_solution(current_solution)
        best_cost = current_cost
        
        if self.verbose:
            print(f"Costo inicial: {current_cost:.2f}")
        
        # Loop principal
        while not self.should_terminate(temperature, self.iterations):
            # Generar solución vecina
            neighbor_solution = self.problem.generate_neighbor(current_solution)
            neighbor_cost = self.problem.calculate_cost(neighbor_solution)
            
            # Calcular probabilidad de aceptación
            prob = self.acceptance_probability(current_cost, neighbor_cost, temperature)
            
            # Decidir si aceptar la nueva solución
            if random.random() < prob:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                self.accepted_moves += 1
                
                # Actualizar mejor solución global
                if current_cost < best_cost:
                    best_solution = self.problem.copy_solution(current_solution)
                    best_cost = current_cost
            else:
                self.rejected_moves += 1
            
            # Registrar estadísticas
            self.temperature_history.append(temperature)
            self.cost_history.append(current_cost)
            self.best_cost_history.append(best_cost)
            
            # Enfriar
            temperature *= self.cooling_rate
            self.iterations += 1
            
            # Mostrar progreso
            if self.verbose and self.iterations % self.progress_interval == 0:
                acceptance_rate = self.accepted_moves / (self.accepted_moves + self.rejected_moves) * 100
                print(f"Iter: {self.iterations:6d} | T: {temperature:8.3f} | "
                      f"Costo: {current_cost:8.2f} | Mejor: {best_cost:8.2f} | "
                      f"Aceptación: {acceptance_rate:5.1f}%")
        
        # Estadísticas finales
        total_moves = self.accepted_moves + self.rejected_moves
        final_acceptance_rate = self.accepted_moves / total_moves * 100 if total_moves > 0 else 0
        
        statistics = {
            'iterations': self.iterations,
            'final_temperature': temperature,
            'accepted_moves': self.accepted_moves,
            'rejected_moves': self.rejected_moves,
            'acceptance_rate': final_acceptance_rate,
            'initial_cost': self.cost_history[0] if self.cost_history else current_cost,
            'final_cost': best_cost,
            'improvement': (self.cost_history[0] - best_cost) / self.cost_history[0] * 100 if self.cost_history else 0,
            'temperature_history': self.temperature_history,
            'cost_history': self.cost_history,
            'best_cost_history': self.best_cost_history
        }
        
        if self.verbose:
            print("-" * 50)
            print(f"Optimización completada:")
            print(f"  Iteraciones: {self.iterations}")
            print(f"  Temperatura final: {temperature:.6f}")
            print(f"  Movimientos aceptados: {self.accepted_moves}")
            print(f"  Movimientos rechazados: {self.rejected_moves}")
            print(f"  Tasa de aceptación: {final_acceptance_rate:.1f}%")
            print(f"  Costo inicial: {statistics['initial_cost']:.2f}")
            print(f"  Mejor costo: {best_cost:.2f}")
            print(f"  Mejora: {statistics['improvement']:.2f}%")
        
        return best_solution, best_cost, statistics


class MultiRunSimulatedAnnealing:
    """
    Ejecutor de múltiples ejecuciones de Simulated Annealing para análisis estadístico.
    """
    
    def __init__(self, problem: OptimizationProblem, sa_params: Dict):
        """
        Args:
            problem: Problema a optimizar
            sa_params: Parámetros para SimulatedAnnealing
        """
        self.problem = problem
        self.sa_params = sa_params
    
    def run_multiple(self, num_runs: int, seed: Optional[int] = None) -> Dict:
        """
        Ejecuta múltiples ejecuciones independientes del algoritmo.
        
        Args:
            num_runs: Número de ejecuciones independientes
            seed: Semilla para reproducibilidad (None para aleatorio)
            
        Returns:
            Diccionario con resultados estadísticos
        """
        if seed is not None:
            random.seed(seed)
        
        results = {
            'solutions': [],
            'costs': [],
            'statistics': [],
            'best_solution': None,
            'best_cost': float('inf'),
            'worst_cost': float('-inf'),
            'mean_cost': 0,
            'std_cost': 0,
            'mean_improvement': 0,
            'std_improvement': 0
        }
        
        print(f"Ejecutando {num_runs} ejecuciones independientes...")
        
        for run in range(num_runs):
            print(f"\n--- Ejecución {run + 1}/{num_runs} ---")
            
            # Crear nuevo optimizador para cada ejecución
            sa = SimulatedAnnealing(self.problem, **self.sa_params, verbose=False)
            solution, cost, stats = sa.optimize()
            
            # Guardar resultados
            results['solutions'].append(solution)
            results['costs'].append(cost)
            results['statistics'].append(stats)
            
            # Actualizar mejor resultado
            if cost < results['best_cost']:
                results['best_cost'] = cost
                results['best_solution'] = self.problem.copy_solution(solution)
            
            # Actualizar peor resultado
            if cost > results['worst_cost']:
                results['worst_cost'] = cost
            
            print(f"Costo: {cost:.2f}, Mejora: {stats['improvement']:.2f}%")
        
        # Calcular estadísticas finales
        costs = results['costs']
        improvements = [s['improvement'] for s in results['statistics']]
        
        results['mean_cost'] = sum(costs) / len(costs)
        results['std_cost'] = math.sqrt(sum((c - results['mean_cost'])**2 for c in costs) / len(costs))
        results['mean_improvement'] = sum(improvements) / len(improvements)
        results['std_improvement'] = math.sqrt(sum((i - results['mean_improvement'])**2 for i in improvements) / len(improvements))
        
        print(f"\n" + "="*60)
        print(f"RESULTADOS ESTADÍSTICOS ({num_runs} ejecuciones)")
        print(f"="*60)
        print(f"Mejor costo: {results['best_cost']:.2f}")
        print(f"Peor costo: {results['worst_cost']:.2f}")
        print(f"Costo promedio: {results['mean_cost']:.2f} ± {results['std_cost']:.2f}")
        print(f"Mejora promedio: {results['mean_improvement']:.2f}% ± {results['std_improvement']:.2f}%")
        
        return results


# Funciones de utilidad

def plot_optimization_progress(statistics: Dict, title: str = "Progreso de Optimización"):
    """
    Grafica el progreso de la optimización.
    
    Args:
        statistics: Diccionario de estadísticas de SimulatedAnnealing
        title: Título del gráfico
    """
    try:
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        iterations = list(range(len(statistics['cost_history'])))
        
        # Gráfico de costo
        ax1.plot(iterations, statistics['cost_history'], 'b-', alpha=0.7, label='Costo Actual')
        ax1.plot(iterations, statistics['best_cost_history'], 'r-', linewidth=2, label='Mejor Costo')
        ax1.set_xlabel('Iteraciones')
        ax1.set_ylabel('Costo')
        ax1.set_title(f'{title} - Evolución del Costo')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de temperatura
        ax2.plot(iterations, statistics['temperature_history'], 'g-', linewidth=2, label='Temperatura')
        ax2.set_xlabel('Iteraciones')
        ax2.set_ylabel('Temperatura')
        ax2.set_title('Enfriamiento de la Temperatura')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')  # Escala logarítmica para la temperatura
        
        plt.tight_layout()
        plt.show()
        
    except ImportError:
        print("matplotlib no está disponible. No se puede mostrar el gráfico.")