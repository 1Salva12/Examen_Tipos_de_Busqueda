# Puzzle lineal con busqueda en profundidad recursiva
from arbol import Nodo
def buscar_Solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        #expandir nodos sucesores(hijos)
        dato_nodo = nodo_inicial.get_datos()
        #hijo izquierdo
        hijo =[dato_nodo [1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo)
        
        #hijo central
        hijo =[dato_nodo [0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_central = Nodo(hijo)
        
        #hijo Derecho
        hijo =[dato_nodo [0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_derecho = Nodo(hijo)
        nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])
        
        for nodo_hijo in nodo_inicial.get_hijos():
            if not nodo_hijo.get_datos() in visitados:
                # Llamada Recursiva
                sol = buscar_Solucion_DFS_rec(nodo_hijo, solucion, visitados)
                if sol != None:
                    return sol
        return None
if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    visitados = []
    nodo_inicial = Nodo(estado_inicial)
    nodo = buscar_Solucion_DFS_rec(nodo_inicial, solucion, visitados)
    #mostar el resultado 
    resultado = []
    if nodo:
        resultado = []
        curr = nodo
        while curr is not None:
            resultado.append(curr.get_datos())
            curr = curr.get_padre()
        
        resultado.reverse()
        print("Camino encontrado:")
        for paso in resultado:
            print(paso)