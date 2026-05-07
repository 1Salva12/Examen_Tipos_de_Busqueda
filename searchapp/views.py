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
    # Grafos de datos
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

    # Valores por defecto para los formularios
    context = {
        "initial_state_text": "4,2,3,1",
        "solution_state_text": "1,2,3,4",
        "bfs_start": "Jiloyork",
        "bfs_goal": "Zacatecas",
        "ucs_start": "jiloyork",
        "ucs_goal": "AGS",
        "mostrar_resultados": False
    }

    if request.method == "POST":
        context["mostrar_resultados"] = True
        
        # Actualizar valores con lo enviado por el usuario
        context.update({
            "initial_state_text": request.POST.get("initial_state"),
            "solution_state_text": request.POST.get("solution_state"),
            "bfs_start": request.POST.get("bfs_start"),
            "bfs_goal": request.POST.get("bfs_goal"),
            "ucs_start": request.POST.get("ucs_start"),
            "ucs_goal": request.POST.get("ucs_goal"),
        })

        # 1. Ejecutar Puzzle (DFS Rec)
        try:
            init = parse_estado_lista(context["initial_state_text"])
            goal = parse_estado_lista(context["solution_state_text"])
            nodo_puzzle = buscar_solucion_DFS_rec(Nodo(init), goal, [])
            context["puzzle_res"] = reconstruir_camino(nodo_puzzle) if nodo_puzzle else None
        except Exception as e:
            context["puzzle_error"] = str(e)

        # 2. Ejecutar Vuelos (BFS)
        try:
            nodo_bfs = buscar_solucion_BFS(conexiones_bfs, context["bfs_start"].strip(), context["bfs_goal"].strip())
            context["bfs_res"] = reconstruir_camino(nodo_bfs) if nodo_bfs else None
        except Exception as e:
            context["bfs_error"] = str(e)

        # 3. Ejecutar Carretera (UCS)
        try:
            nodo_ucs = buscar_solucion_UCS(conexiones_ucs, context["ucs_start"].strip(), context["ucs_goal"].strip())
            if nodo_ucs:
                context["ucs_res"] = reconstruir_camino(nodo_ucs)
                context["ucs_costo"] = nodo_ucs.get_costo()
        except Exception as e:
            context["ucs_error"] = str(e)

    return render(request, "searchapp/index.html", context)