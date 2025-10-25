"""
Implementación QUBO del TSP usando Simulated Annealing

QUBO (Quadratic Unconstrained Binary Optimization) formula el TSP como un problema
de optimización binaria donde cada variable x_{i,j} indica si la ciudad i es 
visitada en la posición j del tour.

La función objetivo incluye:
1. Minimizar distancias: Σ d_{ij} * x_{i,k} * x_{j,k+1}
2. Constraint: cada ciudad visitada exactamente una vez: Σ_k x_{i,k} = 1
3. Constraint: cada posición ocupada por exactamente una ciudad: Σ_i x_{i,k} = 1

Autor: Sistema de Optimización Cuántica
Fecha: Octubre 2025
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Any
from simulated_annealing import OptimizationProblem
import tsp_base as tsp


class TSPQUBO(OptimizationProblem):
    """
    Implementación QUBO del TSP que hereda de OptimizationProblem.
    
    En esta formulación:
    - Una solución es una matriz binaria n×n donde x[i][j] = 1 si la ciudad i 
      está en la posición j del tour
    - El costo incluye la distancia del tour + penalizaciones por constraint violations
    - Los vecinos se generan modificando la asignación binaria
    """
    
    def __init__(self, ciudades: Dict[str, Tuple[int, int]], 
                 penalty_factor: float = 1000.0,
                 constraint_weight: float = 1.0):
        """
        Inicializa el problema TSP QUBO.
        
        Args:
            ciudades: Diccionario {nombre_ciudad: (x, y)}
            penalty_factor: Factor de penalización para violaciones de constraints
            constraint_weight: Peso relativo de los constraints vs distancia
        """
        self.ciudades = ciudades
        self.nombres_ciudades = list(ciudades.keys())
        self.n = len(self.nombres_ciudades)
        self.penalty_factor = penalty_factor
        self.constraint_weight = constraint_weight
        
        # Crear mapeo de nombres a índices
        self.nombre_a_indice = {nombre: i for i, nombre in enumerate(self.nombres_ciudades)}
        self.indice_a_nombre = {i: nombre for i, nombre in enumerate(self.nombres_ciudades)}
        
        # Pre-calcular matriz de distancias usando índices
        self.D = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    ciudad_i = self.nombres_ciudades[i]
                    ciudad_j = self.nombres_ciudades[j]
                    self.D[i][j] = tsp.calcular_distancia_euclidiana(
                        self.ciudades[ciudad_i], self.ciudades[ciudad_j])
        
        # Crear matriz QUBO
        self._build_qubo_matrix()
    
    def _build_qubo_matrix(self):
        """
        Construye la matriz QUBO Q para el problema TSP.
        
        La formulación QUBO es:
        E(x) = x^T Q x
        
        Donde Q incluye:
        1. Términos de distancia
        2. Penalizaciones por constraint violations
        """
        # Tamaño de la matriz QUBO (n² variables)
        size = self.n * self.n
        self.Q = np.zeros((size, size))
        
        # Función auxiliar para convertir (i,j) a índice lineal
        def var_index(i, j):
            return i * self.n + j
        
        # 1. Términos de distancia del tour
        # Σ_{i,j,k} d_{ij} * x_{i,k} * x_{j,(k+1)%n}
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    for k in range(self.n):
                        idx1 = var_index(i, k)
                        idx2 = var_index(j, (k + 1) % self.n)
                        
                        if idx1 == idx2:
                            # Término diagonal
                            self.Q[idx1][idx1] += self.D[i][j]
                        else:
                            # Término fuera de la diagonal (dividir por 2 debido a la simetría)
                            self.Q[idx1][idx2] += self.D[i][j] / 2
                            self.Q[idx2][idx1] += self.D[i][j] / 2
        
        # 2. Constraint: cada ciudad en exactamente una posición
        # Penalización: λ * (Σ_j x_{i,j} - 1)²
        for i in range(self.n):
            for j1 in range(self.n):
                for j2 in range(self.n):
                    idx1 = var_index(i, j1)
                    idx2 = var_index(i, j2)
                    
                    if idx1 == idx2:
                        # Término lineal: -2λ * x_{i,j}
                        self.Q[idx1][idx1] += self.penalty_factor * self.constraint_weight * (-2 + 1)
                    else:
                        # Término cuadrático: 2λ * x_{i,j1} * x_{i,j2}
                        self.Q[idx1][idx2] += self.penalty_factor * self.constraint_weight
        
        # 3. Constraint: cada posición ocupada por exactamente una ciudad
        # Penalización: λ * (Σ_i x_{i,j} - 1)²
        for j in range(self.n):
            for i1 in range(self.n):
                for i2 in range(self.n):
                    idx1 = var_index(i1, j)
                    idx2 = var_index(i2, j)
                    
                    if idx1 == idx2:
                        # Término lineal: -2λ * x_{i,j}
                        self.Q[idx1][idx1] += self.penalty_factor * self.constraint_weight * (-2 + 1)
                    else:
                        # Término cuadrático: 2λ * x_{i1,j} * x_{i2,j}
                        self.Q[idx1][idx2] += self.penalty_factor * self.constraint_weight
        
        # Agregar constante para completar los constraints (se suma al final)
        self.constant_term = 2 * self.n * self.penalty_factor * self.constraint_weight
    
    def generate_initial_solution(self) -> np.ndarray:
        """
        Genera una solución inicial aleatoria válida.
        
        Returns:
            Matriz binaria n×n representando un tour válido
        """
        # Generar permutación aleatoria
        permutacion = list(range(self.n))
        random.shuffle(permutacion)
        
        # Convertir a matriz binaria
        x = np.zeros((self.n, self.n), dtype=int)
        for pos, ciudad in enumerate(permutacion):
            x[ciudad][pos] = 1
        
        return x
    
    def generate_initial_solution_greedy(self) -> np.ndarray:
        """
        Genera una solución inicial usando el algoritmo greedy.
        
        Returns:
            Matriz binaria n×n usando nearest neighbor
        """
        # Usar algoritmo greedy de la formulación clásica
        ruta_nombres = tsp.generar_ruta_greedy_nearest_neighbor(self.ciudades)
        
        # Convertir a matriz binaria
        x = np.zeros((self.n, self.n), dtype=int)
        for pos, nombre in enumerate(ruta_nombres):
            ciudad_idx = self.nombre_a_indice[nombre]
            x[ciudad_idx][pos] = 1
        
        return x
    
    def calculate_cost(self, solution: np.ndarray) -> float:
        """
        Calcula el costo QUBO de una solución.
        
        Args:
            solution: Matriz binaria n×n
            
        Returns:
            Valor de la función objetivo QUBO
        """
        # Vectorizar la matriz
        x_vector = solution.flatten()
        
        # Calcular E(x) = x^T Q x + constante
        energy = np.dot(x_vector, np.dot(self.Q, x_vector)) + self.constant_term
        
        return energy
    
    def calculate_tour_cost(self, solution: np.ndarray) -> float:
        """
        Calcula solo el costo del tour (sin penalizaciones).
        
        Args:
            solution: Matriz binaria n×n
            
        Returns:
            Distancia total del tour
        """
        ruta = self.solution_to_route(solution)
        if ruta is None:
            return float('inf')
        
        return tsp.calcular_costo_ruta(ruta, self.ciudades)
    
    def solution_to_route(self, solution: np.ndarray) -> List[str]:
        """
        Convierte una solución QUBO a una ruta de ciudades.
        
        Args:
            solution: Matriz binaria n×n
            
        Returns:
            Lista de nombres de ciudades o None si es inválida
        """
        try:
            ruta = []
            for pos in range(self.n):
                ciudades_en_pos = [i for i in range(self.n) if solution[i][pos] == 1]
                if len(ciudades_en_pos) != 1:
                    return None  # Posición inválida
                ruta.append(self.indice_a_nombre[ciudades_en_pos[0]])
            
            # Verificar que todas las ciudades estén presentes
            if set(ruta) != set(self.nombres_ciudades):
                return None
            
            return ruta
        except:
            return None
    
    def route_to_solution(self, ruta: List[str]) -> np.ndarray:
        """
        Convierte una ruta de ciudades a una solución QUBO.
        
        Args:
            ruta: Lista de nombres de ciudades
            
        Returns:
            Matriz binaria n×n
        """
        x = np.zeros((self.n, self.n), dtype=int)
        for pos, nombre in enumerate(ruta):
            ciudad_idx = self.nombre_a_indice[nombre]
            x[ciudad_idx][pos] = 1
        
        return x
    
    def generate_neighbor(self, solution: np.ndarray) -> np.ndarray:
        """
        Genera una solución vecina modificando la asignación binaria.
        
        Args:
            solution: Matriz binaria actual
            
        Returns:
            Nueva matriz binaria vecina
        """
        # Diferentes estrategias para generar vecinos
        strategy = random.choice(['swap_positions', 'swap_cities', 'cycle_shift'])
        
        if strategy == 'swap_positions':
            return self._swap_positions_neighbor(solution)
        elif strategy == 'swap_cities':
            return self._swap_cities_neighbor(solution)
        else:  # cycle_shift
            return self._cycle_shift_neighbor(solution)
    
    def _swap_positions_neighbor(self, solution: np.ndarray) -> np.ndarray:
        """
        Genera vecino intercambiando dos posiciones en el tour.
        """
        vecino = solution.copy()
        
        # Seleccionar dos posiciones aleatorias
        pos1, pos2 = random.sample(range(self.n), 2)
        
        # Intercambiar las columnas
        vecino[:, [pos1, pos2]] = vecino[:, [pos2, pos1]]
        
        return vecino
    
    def _swap_cities_neighbor(self, solution: np.ndarray) -> np.ndarray:
        """
        Genera vecino intercambiando dos ciudades en el tour.
        """
        vecino = solution.copy()
        
        # Seleccionar dos ciudades aleatorias
        city1, city2 = random.sample(range(self.n), 2)
        
        # Intercambiar las filas
        vecino[[city1, city2], :] = vecino[[city2, city1], :]
        
        return vecino
    
    def _cycle_shift_neighbor(self, solution: np.ndarray) -> np.ndarray:
        """
        Genera vecino aplicando un corrimiento cíclico a un segmento.
        """
        vecino = solution.copy()
        
        # Seleccionar segmento aleatorio
        start = random.randint(0, self.n-2)
        length = random.randint(2, self.n-start)
        end = start + length
        
        # Aplicar corrimiento cíclico a las columnas
        if end <= self.n:
            segment = vecino[:, start:end].copy()
            vecino[:, start:end] = np.roll(segment, 1, axis=1)
        
        return vecino
    
    def copy_solution(self, solution: np.ndarray) -> np.ndarray:
        """
        Crea una copia profunda de la solución.
        
        Args:
            solution: Matriz binaria a copiar
            
        Returns:
            Copia independiente de la matriz
        """
        return solution.copy()
    
    def validate_solution(self, solution: np.ndarray) -> bool:
        """
        Valida que una solución QUBO sea correcta.
        
        Args:
            solution: Matriz binaria a validar
            
        Returns:
            True si la solución es válida
        """
        # Verificar dimensiones
        if solution.shape != (self.n, self.n):
            return False
        
        # Verificar que solo contenga 0s y 1s
        if not np.all(np.isin(solution, [0, 1])):
            return False
        
        # Verificar constraint: cada fila suma 1 (cada ciudad en una posición)
        if not np.all(np.sum(solution, axis=1) == 1):
            return False
        
        # Verificar constraint: cada columna suma 1 (cada posición con una ciudad)
        if not np.all(np.sum(solution, axis=0) == 1):
            return False
        
        return True
    
    def constraint_violations(self, solution: np.ndarray) -> Dict[str, int]:
        """
        Cuenta las violaciones de constraints en una solución.
        
        Args:
            solution: Matriz binaria a evaluar
            
        Returns:
            Diccionario con tipos y números de violaciones
        """
        violations = {
            'cities_constraint': 0,  # Ciudades no en exactamente una posición
            'positions_constraint': 0,  # Posiciones no con exactamente una ciudad
            'total_violations': 0
        }
        
        # Contar violaciones de constraint de ciudades
        for i in range(self.n):
            if np.sum(solution[i, :]) != 1:
                violations['cities_constraint'] += 1
        
        # Contar violaciones de constraint de posiciones
        for j in range(self.n):
            if np.sum(solution[:, j]) != 1:
                violations['positions_constraint'] += 1
        
        violations['total_violations'] = (violations['cities_constraint'] + 
                                        violations['positions_constraint'])
        
        return violations
    
    def get_solution_info(self, solution: np.ndarray) -> Dict[str, Any]:
        """
        Obtiene información detallada sobre una solución QUBO.
        
        Args:
            solution: Matriz binaria a analizar
            
        Returns:
            Diccionario con información de la solución
        """
        qubo_cost = self.calculate_cost(solution)
        tour_cost = self.calculate_tour_cost(solution)
        violations = self.constraint_violations(solution)
        ruta = self.solution_to_route(solution)
        is_valid = self.validate_solution(solution)
        
        penalty_cost = qubo_cost - tour_cost if is_valid else qubo_cost - tour_cost
        
        return {
            'qubo_cost': qubo_cost,
            'tour_cost': tour_cost,
            'penalty_cost': penalty_cost,
            'is_valid': is_valid,
            'violations': violations,
            'route': ruta,
            'matrix_shape': solution.shape,
            'num_ones': np.sum(solution),
            'expected_ones': self.n
        }


def ejemplo_uso_tsp_qubo():
    """
    Ejemplo de uso de la implementación QUBO del TSP.
    """
    print("=== EJEMPLO TSP QUBO ===")
    
    # Generar ciudades de prueba (menos ciudades para QUBO)
    num_ciudades = 8
    mapa_size = 200
    ciudades = tsp.generar_ciudades_clusters(num_ciudades, mapa_size, num_clusters=3)
    
    print(f"Generadas {num_ciudades} ciudades en clusters")
    print(f"Tamaño de la matriz QUBO: {num_ciudades*num_ciudades} × {num_ciudades*num_ciudades}")
    
    # Crear problema TSP QUBO
    problema_qubo = TSPQUBO(ciudades, penalty_factor=1000.0)
    
    # Generar solución inicial
    solucion_inicial = problema_qubo.generate_initial_solution_greedy()
    info_inicial = problema_qubo.get_solution_info(solucion_inicial)
    
    print(f"\nSolución inicial (greedy):")
    print(f"  QUBO cost: {info_inicial['qubo_cost']:.2f}")
    print(f"  Tour cost: {info_inicial['tour_cost']:.2f}")
    print(f"  Penalty cost: {info_inicial['penalty_cost']:.2f}")
    print(f"  Válida: {info_inicial['is_valid']}")
    print(f"  Violaciones: {info_inicial['violations']}")
    
    # Mostrar ruta
    if info_inicial['route']:
        print(f"  Ruta: {' -> '.join(info_inicial['route'])} -> {info_inicial['route'][0]}")
    
    # Mostrar matriz QUBO (solo para problemas pequeños)
    print(f"\nMatriz binaria {num_ciudades}×{num_ciudades}:")
    print(solucion_inicial)
    
    # Generar algunos vecinos para demostrar
    print(f"\nGenerando vecinos...")
    for i in range(3):
        vecino = problema_qubo.generate_neighbor(solucion_inicial)
        info_vecino = problema_qubo.get_solution_info(vecino)
        print(f"  Vecino {i+1}: QUBO={info_vecino['qubo_cost']:.2f}, "
              f"Tour={info_vecino['tour_cost']:.2f}, Válido={info_vecino['is_valid']}")
    
    # Mostrar visualización
    print(f"\nMostrando mapa...")
    tsp.mostrar_mapa_ciudades(ciudades, f"Ciudades para QUBO ({num_ciudades} ciudades)")
    
    if info_inicial['route']:
        tsp.mostrar_ruta(info_inicial['route'], ciudades, "Ruta inicial QUBO", 
                        mostrar_nombres=True)
    
    return problema_qubo, solucion_inicial


if __name__ == "__main__":
    ejemplo_uso_tsp_qubo()