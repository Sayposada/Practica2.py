import heapq

class GrafoNoDirigido:
    def __init__(self):
        self.grafico_dict = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.grafico_dict:
            self.grafico_dict[vertice] = []

    def agregar_arista(self, arista):
        inicio = arista.get_inicio()
        fin = arista.get_fin()
        peso = arista.get_peso()
        tiempo = arista.get_tiempo()

        if inicio not in self.grafico_dict:
            print(f"El vértice {inicio} no existe")
            return
        if fin not in self.grafico_dict:
            print(f"El vértice {fin} no existe")
            return

        # Agregar en ambas direcciones para que sea un grafo no dirigido
        self.grafico_dict[inicio].append((fin, peso, tiempo))
        self.grafico_dict[fin].append((inicio, peso, tiempo))
    
    def __str__(self):
        todas_aristas = []
        for origen, conexiones in self.grafico_dict.items():
            for destino, distancia, tiempo in conexiones:
                todas_aristas.append(f"{origen} --({distancia} km, {tiempo} min)--> {destino}")
        return "\n".join(todas_aristas)
    
    def estan_conectadas_directamente(self, ciudad1, ciudad2):
        if ciudad1 in self.grafico_dict:
            conexiones = [dest for dest, _, _ in self.grafico_dict[ciudad1]]
            return conexiones.count(ciudad2) == 1
        return False

    def camino_mas_corto_distancia(self, inicio, fin):
        return self.dijkstra(inicio, fin, criterio="distancia")

    def camino_mas_corto_tiempo(self, inicio, fin):
        return self.dijkstra(inicio, fin, criterio="tiempo")

    def dijkstra(self, inicio, fin, criterio="distancia"):
        if inicio not in self.grafico_dict or fin not in self.grafico_dict:
            return f"No hay conexión entre {inicio} y {fin}"

        peso_index = 1 if criterio == "distancia" else 2
        heap = [(0, inicio, [])]
        visitados = set()

        while heap:
            peso_actual, nodo_actual, camino = heapq.heappop(heap)

            if nodo_actual in visitados:
                continue
            visitados.add(nodo_actual)

            camino = camino + [nodo_actual]

            if nodo_actual == fin:
                return f"Mejor camino ({criterio}): {' -> '.join(camino)} con {peso_actual} {criterio}"

            for vecino, distancia, tiempo in self.grafico_dict.get(nodo_actual, []):
                if vecino not in visitados:
                    heapq.heappush(heap, (peso_actual + (distancia if criterio == "distancia" else tiempo), vecino, camino))

        return f"No hay ruta entre {inicio} y {fin}"

class Arista:
    def __init__(self, inicio, fin, peso, tiempo):
        self.inicio = inicio
        self.fin = fin
        self.peso = peso
        self.tiempo = tiempo

    def get_inicio(self):
        return self.inicio

    def get_fin(self):
        return self.fin

    def get_peso(self):
        return self.peso

    def get_tiempo(self):
        return self.tiempo


def construir_grafo(nombre_archivo="DatosVias.txt"):
    grafo = GrafoNoDirigido()
    
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split(";")
            if len(datos) < 4:
                continue

            origen, destino = datos[0].strip(), datos[1].strip()
            distancia = int(datos[2]) if datos[2].isdigit() else float('inf')
            tiempo = int(datos[3]) if datos[3].isdigit() else float('inf')

            grafo.agregar_vertice(origen)
            grafo.agregar_vertice(destino)
            grafo.agregar_arista(Arista(origen, destino, distancia, tiempo))
    print(grafo.__str__())
    
    return grafo

if __name__ == "__main__":
    grafo = construir_grafo()
    ciudad_a = input("Ingrese la primera ciudad: ").strip()
    ciudad_b = input("Ingrese la segunda ciudad: ").strip()

    if grafo.estan_conectadas_directamente(ciudad_a, ciudad_b):
        print(f"✅ {ciudad_a} y {ciudad_b} están conectadas por una única carretera.")
    else:
        print(f"❌ {ciudad_a} y {ciudad_b} NO están conectadas directamente.")

    print(grafo.camino_mas_corto_distancia(ciudad_a, ciudad_b))
    print(grafo.camino_mas_corto_tiempo(ciudad_a, ciudad_b))
