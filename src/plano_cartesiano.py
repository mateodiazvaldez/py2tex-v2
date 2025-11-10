def menor_distancia(puntos): #Devuelve tupla
    if len(puntos) == 2: return puntos[0], puntos[1]  #Caso base 2 puntos
    elif len(puntos) == 3:  #Caso base 3 puntos
        #Comparamos todas las distancias y devolvemos pareja con menor distancia
        d1 = medir_distancia_c(puntos[0], puntos[1])
        d2 = medir_distancia_c(puntos[1], puntos[2])
        d3 = medir_distancia_c(puntos[0], puntos[2])
        min_dist = min(d1, d2, d3)
        if min_dist == d1:
            return puntos[0], puntos[1]
        elif min_dist == d2:
            return puntos[1], puntos[2]
        else:
            return puntos[0], puntos[2]
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
