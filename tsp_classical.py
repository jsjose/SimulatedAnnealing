"""
Implementación clásica del TSP usando Simulated Annealing

Esta implementación utiliza la formulación tradicional del TSP donde una solución
es una permutación de ciudades y las operaciones de vecindario son intercambios
como 2-opt, swap, etc.

Autor: Sistema de Optimización Cuántica  
Fecha: Octubre 2025
"""

import random
import copy
from typing import List, Dict, Tuple, Any
from simulated_annealing import OptimizationProblem
import tsp_base as tsp


class TSPClassical(OptimizationProblem):
    """
    Implementación clásica del TSP que hereda de OptimizationProblem.
    
    En esta formulación:
    - Una solución es una lista de nombres de ciudades (permutación)
    - El costo es la distancia total del circuito
    - Los vecinos se generan con operaciones 2-opt, swap, reverse, etc.
    """
    
    def __init__(self, ciudades: Dict[str, Tuple[int, int]], 
                 operacion_vecindario: str = "2opt"):
        """
        Inicializa el problema TSP clásico.
        
        Args:
            ciudades: Diccionario {nombre_ciudad: (x, y)}
            operacion_vecindario: Tipo de operación para generar vecinos
                                 ("2opt", "swap", "reverse", "insert")
        """
        self.ciudades = ciudades
        self.nombres_ciudades = list(ciudades.keys())
        self.operacion_vecindario = operacion_vecindario
        
        # Pre-calcular matriz de distancias para eficiencia
        self.matriz_distancias = tsp.calcular_matriz_distancias(ciudades)
    
    def generate_initial_solution(self) -> List[str]:
        """
        Genera una solución inicial aleatoria.
        
        Returns:
            Lista de nombres de ciudades en orden aleatorio
        """
        return tsp.generar_ruta_aleatoria(self.ciudades)
    
    def generate_initial_solution_greedy(self) -> List[str]:
        """
        Genera una solución inicial usando el algoritmo greedy del vecino más cercano.
        
        Returns:
            Lista de nombres de ciudades usando nearest neighbor
        """
        return tsp.generar_ruta_greedy_nearest_neighbor(self.ciudades)
    
    def calculate_cost(self, solution: List[str]) -> float:
        """
        Calcula el costo de una solución (distancia total del circuito).
        
        Args:
            solution: Lista de nombres de ciudades
            
        Returns:
            Distancia total del circuito
        """
        if len(solution) < 2:
            return 0.0
        
        costo_total = 0.0
        num_ciudades = len(solution)
        
        for i in range(num_ciudades):
            ciudad_actual = solution[i]
            ciudad_siguiente = solution[(i + 1) % num_ciudades]
            costo_total += self.matriz_distancias[(ciudad_actual, ciudad_siguiente)]
        
        return costo_total
    
    def generate_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera una solución vecina usando la operación especificada.
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución vecina
        """
        if self.operacion_vecindario == "2opt":
            return self._2opt_neighbor(solution)
        elif self.operacion_vecindario == "swap":
            return self._swap_neighbor(solution)
        elif self.operacion_vecindario == "reverse":
            return self._reverse_neighbor(solution)
        elif self.operacion_vecindario == "insert":
            return self._insert_neighbor(solution)
        elif self.operacion_vecindario == "mixed":
            return self._mixed_neighbor(solution)
        else:
            # Por defecto usar 2-opt
            return self._2opt_neighbor(solution)
    
    def _2opt_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera vecino usando operación 2-opt (intercambio de segmentos).
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución con 2-opt aplicado
        """
        vecino = solution[:]
        n = len(vecino)
        
        if n < 4:
            return vecino
        
        # Seleccionar dos índices aleatorios
        i, j = random.sample(range(n), 2)
        if i > j:
            i, j = j, i
        
        # Invertir el segmento entre i y j
        vecino[i:j+1] = reversed(vecino[i:j+1])
        
        return vecino
    
    def _swap_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera vecino intercambiando dos ciudades aleatorias.
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución con dos ciudades intercambiadas
        """
        vecino = solution[:]
        n = len(vecino)
        
        if n < 2:
            return vecino
        
        # Seleccionar dos índices aleatorios
        i, j = random.sample(range(n), 2)
        
        # Intercambiar las ciudades
        vecino[i], vecino[j] = vecino[j], vecino[i]
        
        return vecino
    
    def _reverse_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera vecino invirtiendo un segmento aleatorio.
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución con segmento invertido
        """
        vecino = solution[:]
        n = len(vecino)
        
        if n < 3:
            return vecino
        
        # Seleccionar segmento aleatorio
        start = random.randint(0, n-2)
        length = random.randint(2, min(n-start, n//2))
        end = start + length
        
        # Invertir el segmento
        vecino[start:end] = reversed(vecino[start:end])
        
        return vecino
    
    def _insert_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera vecino moviendo una ciudad a una nueva posición.
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución con una ciudad reubicada
        """
        vecino = solution[:]
        n = len(vecino)
        
        if n < 3:
            return vecino
        
        # Seleccionar ciudad a mover y nueva posición
        old_pos = random.randint(0, n-1)
        new_pos = random.randint(0, n-1)
        
        if old_pos != new_pos:
            # Mover la ciudad
            ciudad = vecino.pop(old_pos)
            vecino.insert(new_pos, ciudad)
        
        return vecino
    
    def _mixed_neighbor(self, solution: List[str]) -> List[str]:
        """
        Genera vecino usando una operación aleatoria (mixed approach).
        
        Args:
            solution: Solución actual
            
        Returns:
            Nueva solución usando operación aleatoria
        """
        operaciones = ["2opt", "swap", "reverse", "insert"]
        operacion = random.choice(operaciones)
        
        if operacion == "2opt":
            return self._2opt_neighbor(solution)
        elif operacion == "swap":
            return self._swap_neighbor(solution)
        elif operacion == "reverse":
            return self._reverse_neighbor(solution)
        else:  # insert
            return self._insert_neighbor(solution)
    
    def copy_solution(self, solution: List[str]) -> List[str]:
        """
        Crea una copia profunda de la solución.
        
        Args:
            solution: Solución a copiar
            
        Returns:
            Copia independiente de la solución
        """
        return solution[:]
    
    def validate_solution(self, solution: List[str]) -> bool:
        """
        Valida que una solución sea correcta para el TSP.
        
        Args:
            solution: Solución a validar
            
        Returns:
            True si la solución es válida
        """
        return tsp.validar_ruta(solution, self.ciudades)
    
    def get_solution_info(self, solution: List[str]) -> Dict[str, Any]:
        """
        Obtiene información detallada sobre una solución.
        
        Args:
            solution: Solución a analizar
            
        Returns:
            Diccionario con información de la solución
        """
        costo = self.calculate_cost(solution)
        valida = self.validate_solution(solution)
        
        # Calcular estadísticas de distancias
        distancias = []
        n = len(solution)
        for i in range(n):
            ciudad_actual = solution[i]
            ciudad_siguiente = solution[(i + 1) % n]
            distancias.append(self.matriz_distancias[(ciudad_actual, ciudad_siguiente)])
        
        return {
            'costo_total': costo,
            'valida': valida,
            'num_ciudades': len(solution),
            'distancia_promedio': sum(distancias) / len(distancias) if distancias else 0,
            'distancia_min': min(distancias) if distancias else 0,
            'distancia_max': max(distancias) if distancias else 0,
            'ruta': solution[:],
            'distancias_segmentos': distancias
        }
    
    def local_search_2opt(self, solution: List[str], max_improvements: int = 100) -> List[str]:
        """
        Realiza búsqueda local 2-opt hasta encontrar un óptimo local.
        
        Args:
            solution: Solución inicial
            max_improvements: Máximo número de mejoras a buscar
            
        Returns:
            Solución mejorada (óptimo local)
        """
        current_solution = self.copy_solution(solution)
        current_cost = self.calculate_cost(current_solution)
        improvements = 0
        
        while improvements < max_improvements:
            improved = False
            n = len(current_solution)
            
            # Probar todos los posibles intercambios 2-opt
            for i in range(n-1):
                for j in range(i+2, n):
                    # Crear vecino 2-opt
                    neighbor = current_solution[:]
                    neighbor[i:j+1] = reversed(neighbor[i:j+1])
                    
                    # Evaluar vecino
                    neighbor_cost = self.calculate_cost(neighbor)
                    
                    # Si es mejor, actualizar
                    if neighbor_cost < current_cost:
                        current_solution = neighbor
                        current_cost = neighbor_cost
                        improvements += 1
                        improved = True
                        break
                
                if improved:
                    break
            
            # Si no hay mejora, hemos encontrado óptimo local
            if not improved:
                break
        
        return current_solution


def ejemplo_uso_tsp_classical():
    """
    Ejemplo de uso de la implementación clásica del TSP.
    """
    print("=== EJEMPLO TSP CLÁSICO ===")
    
    # Generar ciudades de prueba
    num_ciudades = 20
    mapa_size = 200
    ciudades = tsp.generar_ciudades_clusters(num_ciudades, mapa_size)
    
    print(f"Generadas {num_ciudades} ciudades en clusters")
    
    # Crear problema TSP
    problema_tsp = TSPClassical(ciudades, operacion_vecindario="2opt")
    
    # Generar solución inicial
    solucion_inicial = problema_tsp.generate_initial_solution_greedy()
    costo_inicial = problema_tsp.calculate_cost(solucion_inicial)
    
    print(f"Solución inicial (greedy): {costo_inicial:.2f}")
    
    # Mostrar información de la solución inicial
    info_inicial = problema_tsp.get_solution_info(solucion_inicial)
    print(f"Distancia promedio por segmento: {info_inicial['distancia_promedio']:.2f}")
    print(f"Segmento más corto: {info_inicial['distancia_min']:.2f}")
    print(f"Segmento más largo: {info_inicial['distancia_max']:.2f}")
    
    # Aplicar búsqueda local 2-opt
    print("\nAplicando búsqueda local 2-opt...")
    solucion_local = problema_tsp.local_search_2opt(solucion_inicial)
    costo_local = problema_tsp.calculate_cost(solucion_local)
    
    mejora_local = (costo_inicial - costo_local) / costo_inicial * 100
    print(f"Después de 2-opt local: {costo_local:.2f} (mejora: {mejora_local:.2f}%)")
    
    # Mostrar mapas
    print("\nMostrando visualizaciones...")
    tsp.mostrar_mapa_ciudades(ciudades, "Ciudades en Clusters")
    tsp.comparar_rutas(solucion_inicial, solucion_local, ciudades, 
                      ("Solución Inicial (Greedy)", "Después de 2-opt Local"))
    
    return problema_tsp, solucion_inicial, solucion_local


if __name__ == "__main__":
    ejemplo_uso_tsp_classical()