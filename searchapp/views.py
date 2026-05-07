from django.shortcuts import render
from .arbol import (
    Nodo,
    buscar_solucion_DFS_rec,
    buscar_solucion_DFS,
    buscar_solucion_UCS,
    reconstruir_camino,
)


def parse_estado_lista(texto):
    texto = texto.strip()
    if not texto:
        return []
    return [int(item.strip()) for item in texto.split(",") if item.strip()]


def index(request):
    conexiones = {
        "jiloyork": {"CDMX": 125, "QRO": 513},
        "MORELOS": {"QRO": 524},
        "CDMX": {"jiloyork": 125, "QRO": 433, "HGO": 401},
        "HGO": {"CDMX": 941, "QRO": 356, "MEXICALI": 309, "MTY": 346},
        "QRO": {
            "SLP": 203,
            "MORELOS": 514,
            "jiloyork": 513,
            "CDMX": 423,
            "MTY": 603,
            "SONORA": 437,
            "HGO": 356,
            "MEXICALI": 313,
            "AGS": 599,
        },
        "SLP": {"AGS": 390, "QRO": 263},
        "AGS": {"SLP": 390, "QRO": 599},
        "SONORA": {"QRO": 437, "MEXICALI": 394},
        "MEXICALI": {"MTY": 296, "HGO": 309, "QRO": 312},
        "MTR": {"MEXICALI": 296, "QRO": 603, "HGO": 346},
    }

    context = {
        "page": "menu",  # menu, form, result
        "selected_option": None,
        "initial_state_text": "4,2,3,1",
        "solution_state_text": "1,2,3,4",
        "ucs_start": "jiloyork",
        "ucs_goal": "AGS",
        "result_path": None,
        "result_cost": None,
        "error_message": None,
    }

    if request.method == "POST":
        # Si el usuario presiona "Volver al menú"
        if "back_to_menu" in request.POST:
            context["page"] = "menu"
            return render(request, "searchapp/index.html", context)
        
        # Si elige una opción del menú
        if "select_search" in request.POST:
            option = request.POST.get("search_option")
            if option:
                context["selected_option"] = option
                context["page"] = "form"
            else:
                context["page"] = "menu"
            return render(request, "searchapp/index.html", context)
        
        # Si ejecuta una búsqueda
        option = request.POST.get("task_option")
        context["selected_option"] = option
        context["initial_state_text"] = request.POST.get("initial_state", context["initial_state_text"])
        context["solution_state_text"] = request.POST.get("solution_state", context["solution_state_text"])
        context["ucs_start"] = request.POST.get("ucs_start", context["ucs_start"])
        context["ucs_goal"] = request.POST.get("ucs_goal", context["ucs_goal"])

        try:
            if option == "puzzle_dfs_rec":
                estado_inicial = parse_estado_lista(context["initial_state_text"])
                solucion_lista = parse_estado_lista(context["solution_state_text"])
                nodo = buscar_solucion_DFS_rec(Nodo(estado_inicial), solucion_lista, [])
                context["result_path"] = reconstruir_camino(nodo) if nodo else None

            elif option == "puzzle_dfs_iter":
                estado_inicial = parse_estado_lista(context["initial_state_text"])
                solucion_lista = parse_estado_lista(context["solution_state_text"])
                nodo = buscar_solucion_DFS(estado_inicial, solucion_lista)
                context["result_path"] = reconstruir_camino(nodo) if nodo else None

            elif option == "road_ucs":
                nodo = buscar_solucion_UCS(conexiones, context["ucs_start"].strip(), context["ucs_goal"].strip())
                context["result_path"] = reconstruir_camino(nodo) if nodo else None
                context["result_cost"] = nodo.get_costo() if nodo else None

            else:
                context["error_message"] = "Seleccione una opción válida."

        except ValueError:
            context["error_message"] = "El estado inicial o la solución deben ser listas de números separados por comas."

        context["page"] = "result"

    return render(request, "searchapp/index.html", context)

