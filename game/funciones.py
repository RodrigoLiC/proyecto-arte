def aplicar_gravedad(circulo1, circulo2, G=1):
    # Vector desde circulo1 a circulo2
    direccion = circulo2.posicion - circulo1.posicion
    distancia = direccion.length()

    if distancia == 0:
        return  # Evitar división por cero

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
