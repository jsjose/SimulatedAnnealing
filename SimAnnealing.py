import random
import math

# --- 1. Definición del Problema (Caso de Prueba) ---

# La solución que queremos encontrar
OBJETIVO = "Simulated Annealing"
# Los posibles "átomos" de nuestra solución
CARACTERES = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LONGITUD = len(OBJETIVO)


def calcular_costo(solucion):
    """
    Calcula cuántos caracteres son diferentes del objetivo.
    Un costo más bajo es mejor. El costo 0 es la solución perfecta.
    """
    costo = 0
    for i in range(LONGITUD):
        if solucion[i] != OBJETIVO[i]:
            costo += 1
    return costo

def generar_vecino(solucion):
    """
    Genera una nueva solución (vecino) cambiando un carácter
    aleatorio de la solución actual.
    """
    # Convertimos el string a lista para poder modificarlo
    sol_lista = list(solucion)
    
    # Elegimos un índice y un carácter nuevo al azar
    idx_a_cambiar = random.randint(0, LONGITUD - 1)
    nuevo_caracter = random.choice(CARACTERES)
    
    # Reemplazamos el carácter
    sol_lista[idx_a_cambiar] = nuevo_caracter
    
    # Devolvemos la lista convertida de nuevo a string
    return "".join(sol_lista)

def generar_solucion_inicial():
    """Genera una cadena de texto completamente aleatoria."""
    return "".join(random.choice(CARACTERES) for _ in range(LONGITUD))


# --- 2. Algoritmo de Simulated Annealing (de la explicación anterior) ---

def simulated_annealing(solucion_inicial, T_inicial, T_min, alfa):
    """
    Función principal de SA.
    solucion_inicial: Punto de partida (string aleatorio)
    T_inicial: Temperatura inicial (alta)
    T_min: Temperatura final (baja, criterio de parada)
    alfa: Factor de enfriamiento (ej. 0.995). T_nueva = T_vieja * alfa
    """
    
    T = T_inicial
    solucion_actual = solucion_inicial
    costo_actual = calcular_costo(solucion_actual)
    
    mejor_solucion = solucion_actual
    mejor_costo = costo_actual
    
    # Para ver el progreso
    iteracion = 0

    while T > T_min:
        # Generar un vecino
        solucion_vecina = generar_vecino(solucion_actual)
        costo_vecino = calcular_costo(solucion_vecina)

        # Calcular la diferencia de costo
        delta_costo = costo_vecino - costo_actual

        # Decidir si nos movemos a la nueva solución
        if delta_costo < 0:
            # Es mejor (costo más bajo), la aceptamos siempre
            solucion_actual = solucion_vecina
            costo_actual = costo_vecino
        else:
            # Es peor (costo más alto).
            # La aceptamos con probabilidad P = exp(-delta / T)
            probabilidad = math.exp(-delta_costo / T)
            if random.random() < probabilidad:
                solucion_actual = solucion_vecina
                costo_actual = costo_vecino
        
        # Actualizar la mejor solución global si es necesario
        if costo_actual < mejor_costo:
            mejor_solucion = solucion_actual
            mejor_costo = costo_actual
            
        # Enfriar la temperatura
        T *= alfa
        
        # Opcional: Imprimir el progreso
        if iteracion % 1000 == 0:
            print(f"T: {T:.2f} | Costo Actual: {costo_actual} | Mejor Costo: {mejor_costo} | Sol: {solucion_actual}")
        
        iteracion += 1
        
        # Si encontramos la solución perfecta, podemos parar
        if mejor_costo == 0:
            break

    return mejor_solucion, mejor_costo

# --- 3. Ejecución del Caso de Prueba ---

if __name__ == "__main__":
    
    # Parámetros de SA
    T_ini = float(LONGITUD)  # Temperatura inicial (proporcional al costo máx.)
    T_fin = 0.001           # Temperatura final
    ratio_enfriamiento = 0.999 # Tasa de enfriamiento (más lenta = mejor)

    # 1. Crear solución inicial
    sol_inicial = generar_solucion_inicial()
    costo_inicial = calcular_costo(sol_inicial)

    print(f"--- Problema: Encontrar la cadena ---")
    print(f"OBJETIVO:          {OBJETIVO}")
    print(f"SOLUCIÓN INICIAL:  {sol_inicial} (Costo: {costo_inicial})\n")
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
    print(f"Mejor Solución: {mejor_sol}")
    print(f"Mejor Costo:    {mejor_cost}")

    if mejor_cost == 0:
        print("¡Éxito! Se encontró la solución óptima. 🏆")
    else:
        print("Se encontró una solución cercana (mínimo local).")