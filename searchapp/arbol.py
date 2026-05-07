class Nodo:
    def __init__(self, datos, padre=None):
        self._datos = datos
        self._padre = padre
        self._hijos = []
        self._costo = 0

    def get_datos(self):
        return self._datos

    def get_padre(self):
        return self._padre

    def set_hijos(self, hijos):
        self._hijos = hijos

    def get_hijos(self):
        return self._hijos

    def set_costo(self, costo):
        self._costo = costo

    def get_costo(self):
        return self._costo

    def en_lista(self, lista):
        return any(self.igual(item) for item in lista)

    def igual(self, otro):
        if isinstance(otro, Nodo):
            return self.get_datos() == otro.get_datos()
        return self.get_datos() == otro


def reconstruir_camino(nodo):
    camino = []
    actual = nodo
    while actual is not None:
        camino.append(actual.get_datos())
        actual = actual.get_padre()
    camino.reverse()
    return camino


def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato_nodo = nodo_inicial.get_datos()
    sucesores = [
        [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]],
        [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]],
        [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]],
    ]

    hijos = []
    for dato_hijo in sucesores:
        hijo = Nodo(dato_hijo, nodo_inicial)
        hijos.append(hijo)
    nodo_inicial.set_hijos(hijos)

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados:
            sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol

    return None


def buscar_solucion_DFS(estado_inicial, solucion):
    nodo_inicial = Nodo(estado_inicial)
    nodos_visitados = []
    nodos_frontera = [nodo_inicial]

    while nodos_frontera:
        nodo = nodos_frontera.pop()
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()
        sucesores = [
            [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]],
            [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]],
            [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]],
        ]

        hijos = []
        for dato_hijo in sucesores:
            hijo = Nodo(dato_hijo, nodo)
            hijos.append(hijo)
            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo)

        nodo.set_hijos(hijos)

    return None


def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    nodo_inicial = Nodo(estado_inicial)
    nodos_visitados = []
    nodos_frontera = [nodo_inicial]

    while nodos_frontera:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()
        lista_hijos = []
        
        if dato_nodo in conexiones:
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo, nodo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
        
        nodo.set_hijos(lista_hijos)

    return None


def buscar_solucion_UCS(conexiones, estado_inicial, solucion):
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_visitados = []
    nodos_frontera = [nodo_inicial]

    while nodos_frontera:
        nodos_frontera.sort(key=lambda n: n.get_costo())
        nodo = nodos_frontera.pop(0)

        if nodo.get_datos() == solucion:
            return nodo

        nodos_visitados.append(nodo)
        dato_nodo = nodo.get_datos()

        for un_hijo, costo in conexiones.get(dato_nodo, {}).items():
            hijo = Nodo(un_hijo, nodo)
            hijo.set_costo(nodo.get_costo() + costo)

            if hijo.en_lista(nodos_visitados):
                continue

            existente = next((n for n in nodos_frontera if n.igual(hijo)), None)
            if existente:
                if existente.get_costo() > hijo.get_costo():
                    nodos_frontera.remove(existente)
                    nodos_frontera.append(hijo)
            else:
                nodos_frontera.append(hijo)

    return None
