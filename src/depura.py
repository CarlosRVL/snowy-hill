""" depurar.py
Mostrar por pantalla mensaje para depurar. 
Admite una referencia y datos para poder identificar el problema. 
Usar "finalizar=true" para detener la ejecución
"""

def _Depurame_(ref, datos, finalizar=False):
    """
    Uso:
         #_Depurame_(numero,[dato1, dato2,...])
    """
    cadena = "][".join([str(elemento) for elemento in datos])
    print("* Depuracion ref-%d: [%s]" %(ref, cadena))
    if finalizar:
        print ("=== Fin del programa. Se ha llamado a depuracion con orden de finalizar ===")
        exit(1)
