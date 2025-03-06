import heapq
import pandas as pd

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
    
    def imprimir_lista_adyacencia(self):
        for origen, conexiones in self.grafico_dict.items():
            print(f"{origen} -> {', '.join(f'{dest}({dist} km, {time} min)' for dest, dist, time in conexiones)}")
    
    # a. Verificar si hay una única carretera entre A y B
    def estan_conectadas_directamente(self, ciudad1, ciudad2):
        if ciudad1 in self.grafico_dict:
            conexiones = [dest for dest, _, _ in self.grafico_dict[ciudad1]]
            return conexiones.count(ciudad2) == 1
        return False

    # b. Algoritmo de Dijkstra para la menor distancia (KM)
    def camino_mas_corto_distancia(self, inicio, fin):
        return self.dijkstra(inicio, fin, criterio="distancia")

    # c. Algoritmo de Dijkstra para el menor tiempo (MINUTOS)
    def camino_mas_corto_tiempo(self, inicio, fin):
        return self.dijkstra(inicio, fin, criterio="tiempo")

    # Algoritmo de Dijkstra generalizado
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

# Clase Arista
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

# Construcción del grafo desde el archivo de datos
def construir_grafo(nombre_archivo="Datos vias.xlsx"):
    grafo = GrafoNoDirigido()
    df = pd.read_excel(nombre_archivo)
    
    for _, fila in df.iterrows():
        origen = str(fila.iloc[0]).strip()
        destino = str(fila.iloc[1]).strip()
        distancia = int(fila.iloc[2]) if isinstance(fila.iloc[2], (int, float)) else float('inf')
        tiempo = int(fila.iloc[3]) if isinstance(fila.iloc[3], (int, float)) else float('inf')

        grafo.agregar_vertice(origen)
        grafo.agregar_vertice(destino)
        grafo.agregar_arista(Arista(origen, destino, distancia, tiempo))
    
    return grafo

#Menu de opciones para facilitar la muestra
if __name__ == "__main__":
    grafo = construir_grafo()
    
    while True:
        print("\nMenú de opciones:")
        print("1. Imprimir lista de adyacencia")
        print("2. Verificar conexión entre dos ciudades")
        print("3. Mostrar caminos más cortos por distancia y tiempo")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            grafo.imprimir_lista_adyacencia()
        elif opcion == "2":
            ciudad_a = input("Ingrese la primera ciudad: ").strip()
            ciudad_b = input("Ingrese la segunda ciudad: ").strip()
            if grafo.estan_conectadas_directamente(ciudad_a, ciudad_b):
                print(f"✅ {ciudad_a} y {ciudad_b} están conectadas por una única carretera.")
            else:
                print(f"❌ {ciudad_a} y {ciudad_b} NO están conectadas directamente.")
        elif opcion == "3":
            ciudad_a = input("Ingrese la ciudad de origen: ").strip()
            ciudad_b = input("Ingrese la ciudad de destino: ").strip()
            print(grafo.camino_mas_corto_distancia(ciudad_a, ciudad_b))
            print(grafo.camino_mas_corto_tiempo(ciudad_a, ciudad_b))
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intente nuevamente.")
