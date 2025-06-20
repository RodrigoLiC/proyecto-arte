import pygame
import sys
import os
from game.objetos import Circulo
from game.crearCirculo import crear_circulo_aleatorio_fuera_de_escena
from game.funciones import *
from game.audio import gestor_audio
import random

pygame.init()
ANCHO, ALTO = 1200, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Huellas")

# Inicializar sistema de audio
duracion_simulacion_segundos = 120  # Duración por defecto
if gestor_audio.inicializar_audio():
    if gestor_audio.cargar_musica_desde_carpeta():
        print("\n" + "="*60)
        print("🎵 CONFIGURACIÓN DE AUDIO")
        print("="*60)
        duracion_simulacion_segundos = gestor_audio.reproducir_musica_seleccionada()
        print("="*60)
    else:
        print("🔇 Continuando sin música. Coloca archivos de música en la carpeta 'music'.")
        duracion_simulacion_segundos = 120  # Duración por defecto sin música

# Crear un círculo con velocidad hacia la derecha y abajo
circulo = Circulo(x=ANCHO//2, y=ALTO//2, radio=30, masa=0, color=(255, 255, 255), velocidad_x=0, velocidad_y=0)

reloj = pygame.time.Clock()
ejecutando = True
tick = 0

# Control de tiempo basado en la duración de la canción seleccionada
DURACION_SIMULACION = duracion_simulacion_segundos * 60  # Convertir a ticks (60 FPS)
tiempo_inicio = pygame.time.get_ticks()
TIEMPO_LIMITE_MS = duracion_simulacion_segundos * 1000  # Convertir a milisegundos

print(f"⏰ Simulación configurada para {duracion_simulacion_segundos//60}:{duracion_simulacion_segundos%60:02d}")

circulos = [circulo]
fase_simulacion = "activa"
motivo_finalizacion = ""  # Para distinguir entre "musica_terminada" y "tiempo_cumplido"
tiempo_inicio_finalizacion = None  # Para el temporizador de emergencia

circulos[0].setVelLimit(0, 5)


while ejecutando:
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_restante_s = max(0, (TIEMPO_LIMITE_MS - tiempo_transcurrido) // 1000)
    
    # Actualizar audio según el estado de la simulación
    num_conexiones = len(interacciones)
    gestor_audio.actualizar_audio(tiempo_restante_s, num_conexiones)
      # Verificar si la música terminó naturalmente (solo después de 10 segundos para evitar false positives)
    if (tiempo_transcurrido > 10000 and  # Al menos 10 segundos desde el inicio
        not pygame.mixer.music.get_busy() and 
        fase_simulacion == "activa" and
        gestor_audio.musica_actual is not None):  # Asegurar que había música reproduciéndose
        fase_simulacion = "finalizando"
        motivo_finalizacion = "musica_terminada"
        tiempo_inicio_finalizacion = tiempo_actual
        print("🎵 ¡La música terminó! Iniciando eliminación inmediata de círculos...")
    
    # Verificar si se cumplió el tiempo límite (backup por si la música no termina)
    elif tiempo_transcurrido >= TIEMPO_LIMITE_MS and fase_simulacion == "activa":
        fase_simulacion = "finalizando"
        motivo_finalizacion = "tiempo_cumplido"
        tiempo_inicio_finalizacion = tiempo_actual
        gestor_audio.iniciar_fade_final()
        print("⏰ ¡Tiempo cumplido! Iniciando fase de finalización...")
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    if tick % 120 == 0 and fase_simulacion == "activa":
        if len(freelist) > 0:
            circulos[freelist[0]] = crear_circulo_aleatorio_fuera_de_escena(ANCHO, ALTO, radio=30)
            freelist.pop(0)
        else:            circulos.append(crear_circulo_aleatorio_fuera_de_escena(ANCHO, ALTO, radio=30))
    
    if fase_simulacion == "finalizando":
        # Usar eliminación inmediata si la música terminó, gradual si fue por tiempo
        velocidad = "inmediata" if motivo_finalizacion == "musica_terminada" else "normal"
        eliminar_todos_excepto_inicial(circulos, velocidad)
        
        circulos_restantes = sum(1 for c in circulos if c is not None)
        tiempo_finalizando = tiempo_actual - tiempo_inicio_finalizacion        # Salir si solo queda el círculo inicial O si ha pasado demasiado tiempo finalizando (emergencia)
        if circulos_restantes <= 1 or tiempo_finalizando > 10000:  # Máximo 10 segundos finalizando
            if tiempo_finalizando > 10000:
                print("⚠️ Salida de emergencia: Finalizando por tiempo excedido")
            else:
                print("🏁 ¡Simulación completada! Solo queda la bola inicial.")
            print(f"🎯 Motivo de finalización: {motivo_finalizacion}")
            
            # DETENER COMPLETAMENTE EL AUDIO
            pygame.mixer.music.stop()
            gestor_audio.detener_audio()
            
            # Colocar la bola inicial en el centro
            if circulos[0] is not None:
                circulos[0].posicion.x = ANCHO // 2
                circulos[0].posicion.y = ALTO // 2
                circulos[0].velocidad.x = 0
                circulos[0].velocidad.y = 0
            
            # Cambiar a fase final - mantener entorno pero sin nuevas bolas
            fase_simulacion = "completada"
            print("🎯 Simulación completada. Cierra la ventana manualmente cuando quieras salir.")

    ventana.fill((0, 0, 0))
    
    # Mostrar indicador de tiempo restante
    tiempo_restante_s = max(0, (TIEMPO_LIMITE_MS - tiempo_transcurrido) // 1000)
    if fase_simulacion == "activa":
        font = pygame.font.Font(None, 36)
        # Mostrar tiempo restante y duración total
        duracion_total_str = f"{duracion_simulacion_segundos//60}:{duracion_simulacion_segundos%60:02d}"
        tiempo_str = f"{tiempo_restante_s // 60}:{tiempo_restante_s % 60:02d}"
        texto_tiempo = font.render(f"🎵 {tiempo_str} / {duracion_total_str}", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (10, 10))
        
        # Mostrar nombre de la canción actual si hay música
        if gestor_audio.musica_actual:
            font_pequena = pygame.font.Font(None, 24)
            nombre_cancion = os.path.basename(gestor_audio.musica_actual)
            if len(nombre_cancion) > 50:
                nombre_cancion = nombre_cancion[:47] + "..."
            texto_cancion = font_pequena.render(f"♪ {nombre_cancion}", True, (200, 200, 200))
            ventana.blit(texto_cancion, (10, 50))
    elif fase_simulacion == "finalizando":
        font = pygame.font.Font(None, 48)
        texto_finalizando = font.render("🎵 Finalizando simulación...", True, (255, 255, 0))
        ventana.blit(texto_finalizando, (ANCHO//2 - 250, 10))
    elif fase_simulacion == "completada":
        # Mostrar mensaje de simulación completada
        font = pygame.font.Font(None, 48)
        texto_completada = font.render("🏁 ¡SIMULACIÓN COMPLETADA!", True, (0, 255, 0))
        ventana.blit(texto_completada, (ANCHO//2 - 250, 10))
        
        # Mostrar instrucción para cerrar
        font_pequena = pygame.font.Font(None, 24)
        texto_instruccion = font_pequena.render("Cierra la ventana manualmente cuando desees salir", True, (200, 200, 200))
        ventana.blit(texto_instruccion, (ANCHO//2 - 200, 60))    # Solo mostrar líneas de conexión si no estamos en fase completada
    if fase_simulacion != "completada":
        for keys in interacciones.keys():
            li, lj = map(int, keys.split('_'))
            if circulos[li] is None or circulos[lj] is None:
                continue
            # draw line between circles
            pygame.draw.line(ventana, (5, 5, 5), circulos[li].posicion, circulos[lj].posicion, 8)

    # Procesar física y dibujar círculos
    for i in range(len(circulos)):
        if circulos[i] == None:
            continue
        
        # Solo aplicar física si no estamos en fase completada
        if fase_simulacion != "completada":
            for j in range(len(circulos)):
                if i == 0: # circulos[0] es estatico
                    continue
                if circulos[j] == None or i == j:
                    continue
                
                if circulos[i].posicion.distance_to(circulos[j].posicion) > 100:
                    aplicar_gravedad(circulos[i], circulos[j], G=1)

                repulsion(circulos[i], circulos[j], G=4)

                pair_interact(i, j, circulos)

            if i != 0:
                circulos[i].actualizar()
        
        # Siempre dibujar los círculos que existen
        circulos[i].dibujar(ventana)    # Actualizar colores de los círculos
    for circulo in circulos:
        if circulo is None:
            continue
        
        c1 = circulo.colorBase
        c2 = circulo.color
        fraq = 100
        circulo.color = (
            (c1[0] + c2[0]*(fraq-1)) // fraq,
            (c1[1] + c2[1]*(fraq-1)) // fraq,
            (c1[2] + c2[2]*(fraq-1)) // fraq
        )
        k = list(circulo.color)
        max(k)
        # reescalar color
        circulo.color = (
            int(circulo.color[0] * 255 / max(k)),
            int(circulo.color[1] * 255 / max(k)),
            int(circulo.color[2] * 255 / max(k))
        )

        fraq = 40
        if len(circulo.pairs) > 0:
            c3 = [0.0, 0.0, 0.0]
            peso_total = 0.0
            for pair in circulo.pairs:
                if circulos[pair] is None:
                    continue
                peso = getattr(circulos[pair], 'peso_resonancia', 1.0)
                c3[0] += circulos[pair].color[0] * peso
                c3[1] += circulos[pair].color[1] * peso
                c3[2] += circulos[pair].color[2] * peso
                peso_total += peso

            if peso_total > 0:
                c1 = circulo.color
                circulo.color = (
                    int((c1[0]*(fraq - 1) + c3[0]/peso_total) // fraq),
                    int((c1[1]*(fraq - 1) + c3[1]/peso_total) // fraq),
                    int((c1[2]*(fraq - 1) + c3[2]/peso_total) // fraq)
                )
                k = list(circulo.color)
                max_k = max(k)
                circulo.color = (
                    int(circulo.color[0] * 255 / max_k),
                    int(circulo.color[1] * 255 / max_k),
                    int(circulo.color[2] * 255 / max_k)
                )


    # print(interacciones)

    # for circulo in circulos:
    #    if circulo is None:
    #        print("X ", end="")
    #    else:
    #        print("O ", end="")
    # print()    # Solo eliminar círculos fuera de pantalla si no estamos en fase completada
    if fase_simulacion != "completada":
        eliminar_fueras(circulos, ANCHO, ALTO)
    
    # Solo aplicar transición hacia el mouse si no estamos en fase completada
    if fase_simulacion != "completada":
        transicion_hacia_mouse(circulos[0], suavizado=0.1)
        circulos[0].actualizar()
    # En fase completada, mantener el círculo inicial estático en el centro (ya está posicionado)

    pygame.display.flip()
    
    reloj.tick(60)
    tick += 1

# Limpiar recursos de audio
gestor_audio.detener_audio()

pygame.quit()
sys.exit()

