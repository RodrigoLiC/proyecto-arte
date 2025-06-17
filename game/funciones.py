import random
import math

# Diccionario para guardar los estados entre pares
interacciones = {}
freelist = []

def aplicar_gravedad(circulo1, circulo2, G=1):
    # Vector desde circulo1 a circulo2
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia == 0:
        return  # Evitar división por cero
    if distancia < 100:
        return
    # Normalizar dirección
    direccion_normalizada = direccion.normalize()

    # Calcular fuerza de gravedad (modificada)
    aceleracion_magnitud = G * circulo1.masa / (distancia)

    # Vector aceleración hacia circulo2
    aceleracion = direccion_normalizada * aceleracion_magnitud

    # Actualizar velocidad sumando la aceleración
    circulo1.velocidad += aceleracion

def aplicar_resorte(circulo1, circulo2, k=0.1, longitud_reposo=100):
    # Vector desde circulo1 a circulo2
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia == 0:
        return  # Evitar división por cero

    # Calcular elongación: diferencia entre distancia actual y la de reposo
    elongacion = distancia - longitud_reposo

    # Dirección normalizada del resorte
    direccion_normalizada = direccion.normalize()

    # Fuerza de resorte según la ley de Hooke: F = -k * elongación
    fuerza = direccion_normalizada * (k * elongacion)

    # Suponemos masa=1 para simplificar: aceleración = fuerza / masa
    circulo1.velocidad += fuerza

def aplicar_resorte_con_amortiguamiento(circulo1, circulo2, k=0.1, longitud_reposo=100, b=0.05, max_range=1000):
    # Vector desde circulo1 a circulo2
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia > max_range:
        return

    if distancia == 0:
        return  # Evitar división por cero

    # Dirección normalizada
    direccion_normalizada = direccion.normalize()

    # === Fuerza del resorte ===
    elongacion = distancia - longitud_reposo
    fuerza_resorte = direccion_normalizada * (k * elongacion)

    # === Fuerza de amortiguamiento ===
    # Velocidad relativa entre los dos objetos
    velocidad_relativa = circulo1.velocidad - circulo2.velocidad

    # Proyección de la velocidad relativa en la dirección del resorte
    velocidad_en_direccion = velocidad_relativa.dot(direccion_normalizada)

    # Fuerza amortiguadora (opuesta a la dirección del movimiento relativo)
    fuerza_amortiguamiento = -b * velocidad_en_direccion * direccion_normalizada

    # === Fuerza total ===
    fuerza_total = fuerza_resorte + fuerza_amortiguamiento

    # Suponemos masa = 1, o podrías dividir por la masa si lo deseas
    circulo1.velocidad += fuerza_total




def pair_interact(idx1, idx2, circulos):
    global interacciones
    
    if idx1 == idx2:
        return

    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    code = f"{idx1}_{idx2}"

    # Inicialización por defecto
    if code not in interacciones:
        interacciones[code] = [0, 0]

    x = interacciones[code]

    if x[0] == 0:
        distance = (circulos[idx1].posicion - circulos[idx2].posicion).length()

        if (random.random() < 0.01 and distance < 400) \
              or (random.random() < 0.1 and distance < 250) \
                or (distance < 100):
            interacciones[code] = [1, distance]
            circulos[idx1].pairs.append(idx2)
            circulos[idx2].pairs.append(idx1)
        else:
            del interacciones[code]
            return
    else:
        # Incrementar el valor
        interacciones[code] = [interacciones[code][0] + 1, interacciones[code][1] * 1.0005]
        x = interacciones[code][0]

        # Probabilidad de volver a 0: 1 - e^(-x)
        prob = 1 - math.exp(-max(x/600 - 10, 0))
        if random.random() < prob:
            del interacciones[code]
            circulos[idx1].pairs.remove(idx2)
            circulos[idx2].pairs.remove(idx1)
    
    
    if interacciones[code][0] > 0:
        if idx1 != 0:
            aplicar_resorte_con_amortiguamiento(
                        circulos[idx1], circulos[idx2], 
                        k=0.001, b=0.01, longitud_reposo=interacciones[code][1], 
                        max_range=5000
                    )
        if idx2 != 0:
            aplicar_resorte_con_amortiguamiento(
                        circulos[idx2], circulos[idx1], 
                        k=0.001, b=0.01, longitud_reposo=interacciones[code][1], 
                        max_range=5000
                    )

    return


def eliminar_fueras(circulos, ancho_ventana, alto_ventana):
    global interacciones
    global freelist

    for i in range(len(circulos)):
        circulo = circulos[i]

        if circulo is None:
            continue

        if i == 0:
            continue

        x, y = circulo.posicion[0], circulo.posicion[1]
        r = circulo.radio

        is_fuera = (
            x + r < 0 or     # completamente a la izquierda
            x - r > ancho_ventana or  # completamente a la derecha
            y + r < 0 or     # completamente arriba
            y - r > alto_ventana  # completamente abajo
        )

        if is_fuera:
            pairs = circulo.pairs.copy()
            print(f"Eliminando amistad de {i} con: {', '.join(map(str,pairs))}")
            circulos[i] = None
            freelist.append(i)


            for j in pairs:
                li = min(i, j)
                lj = max(i, j)
                
                code = f"{li}_{lj}"
                #print(f"Eliminando amistad {code}")
                if code in interacciones:
                    del interacciones[code]

            print(interacciones.keys())

            for circulo in circulos:
                if circulo is None:
                    print("X ", end="")
                else:
                    print("O ", end="")
            print()
            


def repulsion(circulo1, circulo2, G=1):
    # Vector desde circulo1 a circulo2
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia == 0:
        return
    
    if distancia < 100:
        # Normalizar dirección
        direccion_normalizada = direccion.normalize()

        # Calcular fuerza de repulsión (modificada)
        aceleracion_magnitud = G * circulo1.masa / (distancia ** 2)

        # Vector aceleración hacia circulo2
        aceleracion = direccion_normalizada * aceleracion_magnitud

        # Actualizar velocidad restando la aceleración
        circulo1.velocidad -= aceleracion