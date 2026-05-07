from django.shortcuts import render
from .arbol import (
    Nodo,
    buscar_solucion_DFS_rec,
    buscar_solucion_BFS,
    buscar_solucion_UCS,
    reconstruir_camino,
)

def parse_estado_lista(texto):
    return [int(item.strip()) for item in texto.split(",") if item.strip()]

def index(request):
    # Diccionarios de datos
    conexiones_ucs = {
        "jiloyork": {"CDMX": 125, "QRO": 513},
        "MORELOS": {"QRO": 524},
        "CDMX": {"jiloyork": 125, "QRO": 433, "HGO": 401},
        "HGO": {"CDMX": 941, "QRO": 356, "MEXICALI": 309, "MTY": 346},
        "QRO": {"SLP": 203, "MORELOS": 514, "jiloyork": 513, "CDMX": 423, "MTY": 603, "SONORA": 437, "HGO": 356, "MEXICALI": 313, "AGS": 599},
        "SLP": {"AGS": 390, "QRO": 263},
        "AGS": {"SLP": 390, "QRO": 599},
        "SONORA": {"QRO": 437, "MEXICALI": 394},
        "MEXICALI": {"MTY": 296, "HGO": 309, "QRO": 312},
        "MTY": {"MEXICALI": 296, "QRO": 603, "HGO": 346},
    }

    conexiones_bfs = {
        "Jiloyork": {"Celaya", "CDMX", "Queretaro"},
        "CDMX": {"Jiloyork"},
        "Sonora": {"Zacatecas", "Sinaloa"},
        "Guanajuato": {"Aguascalientes"},
        "Oaxaca": {"Queretaro"},
        "Sinaloa": {"Celaya", "Sonora", "Jiloyork"},
        "Queretaro": {"Monterrey"},
        "Celaya": {"Jiloyork", "Sinaloa"},
        "Zacatecas": {"Sonora", "Monterrey", "Queretaro"},
        "Monterrey": {"Zacatecas", "Sinaloa"},
        "Tamaulipas": {"Queretaro"},
    }

    # Extraer listas de ciudades únicas para los select
    ciudades_bfs = sorted(list(conexiones_bfs.keys()))
    # Para UCS, también incluimos ciudades que solo aparecen como destino
    ciudades_ucs = set(conexiones_ucs.keys())
    for destinos in conexiones_ucs.values():
        ciudades_ucs.update(destinos.keys())
    ciudades_ucs = sorted(list(ciudades_ucs))

    context = {
        "initial_state_text": "4,2,3,1",
        "solution_state_text": "1,2,3,4",
        "bfs_start": "Jiloyork",
        "bfs_goal": "Zacatecas",
        "ucs_start": "jiloyork",
        "ucs_goal": "AGS",
        "ciudades_bfs": ciudades_bfs,
        "ciudades_ucs": ciudades_ucs,
        "mostrar_resultados": False
    }

    if request.method == "POST":
        context["mostrar_resultados"] = True
        
        # Obtener datos del formulario
        context.update({
            "initial_state_text": request.POST.get("initial_state"),
            "solution_state_text": request.POST.get("solution_state"),
            "bfs_start": request.POST.get("bfs_start"),
            "bfs_goal": request.POST.get("bfs_goal"),
            "ucs_start": request.POST.get("ucs_start"),
            "ucs_goal": request.POST.get("ucs_goal"),
        })

        # 1. Puzzle (DFS)
        try:
            init = parse_estado_lista(context["initial_state_text"])
            goal = parse_estado_lista(context["solution_state_text"])
            nodo_p = buscar_solucion_DFS_rec(Nodo(init), goal, [])
            context["puzzle_res"] = reconstruir_camino(nodo_p) if nodo_p else None
        except Exception as e: context["puzzle_error"] = str(e)

        # 2. Vuelos (BFS)
        try:
            nodo_b = buscar_solucion_BFS(conexiones_bfs, context["bfs_start"], context["bfs_goal"])
            context["bfs_res"] = reconstruir_camino(nodo_b) if nodo_b else None
        except Exception as e: context["bfs_error"] = str(e)

        # 3. Carretera (UCS)
        try:
            nodo_u = buscar_solucion_UCS(conexiones_ucs, context["ucs_start"], context["ucs_goal"])
            if nodo_u:
                context["ucs_res"] = reconstruir_camino(nodo_u)
                context["ucs_costo"] = nodo_u.get_costo()
        except Exception as e: context["ucs_error"] = str(e)

    return render(request, "searchapp/index.html", context)