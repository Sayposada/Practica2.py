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

        if inicio not in self.grafico_dict or fin not in self.grafico_dict:
            print(f"Error: uno de los vértices {inicio} o {fin} no existe")
            return

        self.grafico_dict[inicio].append((fin, peso, tiempo))
        self.grafico_dict[fin].append((inicio, peso, tiempo))
    
    def mostrar_lista_adyacencia(self):
        for vertice, conexiones in self.grafico_dict.items():
            conexiones_str = ", ".join([f"({dest}, {dist}km, {tiempo}min)" for dest, dist, tiempo in conexiones])
            print(f"{vertice} -> {conexiones_str}")
    
    # a. Verificar si hay una única carretera entre A y B
    def estan_conectadas_directamente(self, ciudad1, ciudad2):
        return any(dest == ciudad2 for dest, _, _ in self.grafico_dict.get(ciudad1, []))

    # b. Algoritmo de Dijkstra para la menor distancia (KM)
    def camino_mas_corto(self, inicio, fin, criterio="distancia"):
        if inicio not in self.grafico_dict or fin not in self.grafico_dict:
            return f"No hay conexión entre {inicio} y {fin}"

        peso_index = 1 if criterio == "distancia" else 2
        heap = [(0, inicio, [])]
        visitados = {}

        while heap:
            peso_actual, nodo_actual, camino = heapq.heappop(heap)
            if nodo_actual in visitados and visitados[nodo_actual] <= peso_actual:
                continue
            visitados[nodo_actual] = peso_actual
            camino = camino + [nodo_actual]
            if nodo_actual == fin:
                return f"Mejor camino ({criterio}): {' -> '.join(camino)} con {peso_actual} {criterio}"
            for vecino, distancia, tiempo in self.grafico_dict.get(nodo_actual, []):
                nuevo_peso = peso_actual + (distancia if criterio == "distancia" else tiempo)
                if vecino not in visitados or nuevo_peso < visitados[vecino]:
                    heapq.heappush(heap, (nuevo_peso, vecino, camino))
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
    return grafo

def menu():
    grafo = construir_grafo()
    while True:
        print("\nMenú de opciones:")
        print("1. Imprimir lista de adyacencia del grafo")
        print("2. Verificar si dos ciudades tienen un camino directo")
        print("3. Mostrar el recorrido más corto por distancia y tiempo")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            grafo.mostrar_lista_adyacencia()
        elif opcion == "2":
            ciudad_a = input("Ingrese la primera ciudad: ").strip()
            ciudad_b = input("Ingrese la segunda ciudad: ").strip()
            if grafo.estan_conectadas_directamente(ciudad_a, ciudad_b):
                print(f"✅ {ciudad_a} y {ciudad_b} están conectadas directamente.")
            else:
                print(f"❌ {ciudad_a} y {ciudad_b} NO están conectadas directamente.")
        elif opcion == "3":
            ciudad_a = input("Ingrese la ciudad de origen: ").strip()
            ciudad_b = input("Ingrese la ciudad de destino: ").strip()
            print(grafo.camino_mas_corto(ciudad_a, ciudad_b, "distancia"))
            print(grafo.camino_mas_corto(ciudad_a, ciudad_b, "tiempo"))
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.") #Hola

if __name__ == "__main__":
    menu()





