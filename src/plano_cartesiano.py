import random
class Punto:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __repr__(self):
        """Método para una representación legible del objeto Punto."""
        return f"Punto(x={self.x}, y={self.y})"
        
def medir_distancia_c(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

def menor_distancia(puntos): #Devuelve tupla
    if len(puntos) == 2: return puntos[0], puntos[1]  #Caso base 2 puntos
    elif len(puntos) == 3:  #Caso base 3 puntos
        #Comparamos todas las distancias y devolvemos pareja con menor distancia
        d1 = medir_distancia_c(puntos[0], puntos[1])
        d2 = medir_distancia_c(puntos[1], puntos[2])
        d3 = medir_distancia_c(puntos[0], puntos[2])
        match min(d1, d2, d3):
            case r if r == d1: return puntos[0], puntos[1]
            case r if r == d2: return puntos[1], puntos[2]
            case r if r == d3: return puntos[0], puntos[2]
    else:
        #Caso recursivo
        puntos.sort(key=lambda punto: punto.x)
        medio = len(puntos)//2
        #Calculamos la distancia de la solucion izq y derecha
        solucion_izq = menor_distancia(puntos[:medio])
        solucion_der = menor_distancia(puntos[medio:])
        if medir_distancia_c(*solucion_der) < medir_distancia_c(*solucion_izq): mejor_solucion = solucion_der
        else: mejor_solucion = solucion_izq
        #Guardamos los puntos que estan cerca del medio
        puntos_medio = []
        for punto in puntos:
            if punto.x - puntos[medio].x < medir_distancia_c(*mejor_solucion):
                puntos_medio.append(punto)
        puntos_medio.sort(key=lambda punto: punto.y)
        #Buscamos la mejor solucion discriminando por y
        for i in range(len(puntos_medio)-1):
            if (puntos_medio[i+1].y - puntos_medio[i].y)**2 < medir_distancia_c(*mejor_solucion):
                if medir_distancia_c(puntos_medio[i], puntos_medio[i+1]) < medir_distancia_c(*mejor_solucion):
                    mejor_solucion = puntos_medio[i], puntos_medio[i+1]
        return mejor_solucion
            
    
#Para probar (hecho con gpt)
def main():
    """
    Crea un array de 10 objetos Punto con coordenadas aleatorias (0-50)
    y lo ordena por la coordenada X de menor a mayor.
    """
    NUM_PUNTOS = int(input("Ingrese cantidad de puntos: "))
    LIMITE_MAXIMO = 50 # Límite de coordenadas

    # 1. Crear el array de Puntos
    puntos = []
    for _ in range(NUM_PUNTOS):
        # Genera coordenadas aleatorias entre 0 y LIMITE_MAXIMO (ambos inclusive)
        x_aleatorio = random.randint(0, LIMITE_MAXIMO)
        y_aleatorio = random.randint(0, LIMITE_MAXIMO)
        nuevo_punto = Punto(x_aleatorio, y_aleatorio)
        puntos.append(nuevo_punto)

    print("--- Array de Puntos ---")
    print(puntos)
    print("\n Puntos con menor distancia: \n")
    print(menor_distancia(puntos))
    
if __name__ == "__main__":
    main()