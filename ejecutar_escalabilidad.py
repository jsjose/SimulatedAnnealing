#!/usr/bin/env python3
"""
🎯 Ejecutor Simple: Demo de Escalabilidad TSP

Script para ejecutar fácilmente la demo de escalabilidad solicitada.
Genera gráficas: número de ciudades vs costo y número de ciudades vs tiempo.
"""

def ejecutar_demo():
    """Ejecuta la demo de escalabilidad con configuración predefinida."""
    
    print("🚀" * 50)
    print("📈 DEMO DE ESCALABILIDAD TSP: 10-100 CIUDADES")
    print("🚀" * 50)
    print("🎯 Generará gráficas solicitadas:")
    print("   • Número de ciudades vs Costo (Clásico y QUBO)")  
    print("   • Número de ciudades vs Tiempo (Clásico y QUBO)")
    print("🚀" * 50)
    
    try:
        # Importar y ejecutar la demo optimizada
        from demo_escalabilidad_optimizada import main
        main()
        
        print("\n✅ DEMO COMPLETADA EXITOSAMENTE")
        print("📁 Revisa los archivos PNG generados para ver las gráficas")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("🔧 Asegúrate de que todos los archivos estén en el directorio")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        print("🔧 Verifica que las dependencias estén instaladas")

if __name__ == "__main__":
    ejecutar_demo()