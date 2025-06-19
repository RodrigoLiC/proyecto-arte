import pygame
import numpy as np
import math

def generar_tono_ambiente(duracion_segundos=5, frecuencia_base=220, sample_rate=22050):
    frames = int(duracion_segundos * sample_rate)
    arr = np.zeros((frames, 2), dtype=np.int16)
    
    for i in range(frames):
        t = i / sample_rate
        
        onda1 = math.sin(2 * math.pi * frecuencia_base * t) * 0.3
        onda2 = math.sin(2 * math.pi * frecuencia_base * 1.5 * t) * 0.2
        onda3 = math.sin(2 * math.pi * frecuencia_base * 0.75 * t) * 0.15
        
        
        envolvente = 1.0
        if t < 0.1:  
            envolvente = t / 0.1
        elif t > duracion_segundos - 0.1:  
            envolvente = (duracion_segundos - t) / 0.1
        
        muestra = (onda1 + onda2 + onda3) * envolvente * 16000
        
        arr[i][0] = int(muestra)
        arr[i][1] = int(muestra)
    
    return arr

def inicializar_audio():
    """
    Inicializa el sistema de audio y carga la música de fondo
    """
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
        audio_data = generar_tono_ambiente(duracion_segundos=10, frecuencia_base=200)
        
        sound = pygame.sndarray.make_sound(audio_data)
        
        return sound
    except Exception as e:
        print(f"No se pudo inicializar el audio: {e}")
        return None

def reproducir_audio_ambiente(sound):
    if sound:
        try:
            sound.play(loops=-1)  
            pygame.mixer.music.set_volume(0.2)  
        except Exception as e:
            print(f"No se pudo reproducir el audio: {e}")
