import pygame
import os
import glob
import random
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis

class GestorAudio:
    def __init__(self):
        self.volumen_base = 0.5
        self.volumen_actual = self.volumen_base
        self.fade_speed = 0.02
        self.musica_actual = None
        self.lista_musica = []
        self.estado_simulacion = "inicio"
        self.duracion_cancion = 120
        
    def inicializar_audio(self):
        """
        Inicializa el sistema de audio
        """
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            return True
        except Exception as e:
            print(f"No se pudo inicializar el audio: {e}")
            return False
    
    def obtener_duracion_archivo(self, archivo):
        """
        Obtiene la duración de un archivo de audio en segundos
        """
        try:
            audio_file = File(archivo)
            if audio_file is not None and hasattr(audio_file, 'info'):
                return int(audio_file.info.length)
            return 120  # Duración por defecto si no se puede leer
        except Exception as e:
            print(f"Error al obtener duración de {archivo}: {e}")
            return 120  # Duración por defecto
    
    def mostrar_canciones_disponibles(self):
        """
        Muestra las canciones disponibles con sus duraciones
        """
        if not self.lista_musica:
            return
        
        print("\n🎵 Canciones disponibles:")
        print("-" * 60)
        for i, cancion in enumerate(self.lista_musica, 1):
            nombre = os.path.basename(cancion)
            duracion = self.obtener_duracion_archivo(cancion)
            mins = duracion // 60
            segs = duracion % 60
            print(f"{i:2d}. {nombre:<40} ({mins}:{segs:02d})")
        print("-" * 60)
    
    def seleccionar_cancion_interactiva(self):
        """
        Permite al usuario seleccionar una canción específica
        """
        if not self.lista_musica:
            return None, 120
        
        if len(self.lista_musica) == 1:
            cancion = self.lista_musica[0]
            duracion = self.obtener_duracion_archivo(cancion)
            print(f"🎵 Usando: {os.path.basename(cancion)} ({duracion//60}:{duracion%60:02d})")
            return cancion, duracion
        
        self.mostrar_canciones_disponibles()
        
        while True:
            try:
                print("\nOpciones:")
                print("• Presiona ENTER para selección aleatoria")
                print("• Escribe el número de la canción que quieres")
                print("• Escribe 'q' para salir")
                
                entrada = input("\n🎯 Tu elección: ").strip()
                
                if entrada.lower() == 'q':
                    return None, 120
                
                if entrada == "":
                    # Selección aleatoria
                    cancion = random.choice(self.lista_musica)
                    duracion = self.obtener_duracion_archivo(cancion)
                    print(f"🎲 Selección aleatoria: {os.path.basename(cancion)} ({duracion//60}:{duracion%60:02d})")
                    return cancion, duracion
                
                seleccion = int(entrada)
                if 1 <= seleccion <= len(self.lista_musica):
                    cancion = self.lista_musica[seleccion - 1]
                    duracion = self.obtener_duracion_archivo(cancion)
                    print(f"✅ Seleccionaste: {os.path.basename(cancion)} ({duracion//60}:{duracion%60:02d})")
                    return cancion, duracion
                else:
                    print(f"❌ Por favor, selecciona un número entre 1 y {len(self.lista_musica)}")
                    
            except ValueError:
                print("❌ Por favor, ingresa un número válido o presiona ENTER")
            except KeyboardInterrupt:
                print("\n🚫 Cancelado. Usando selección aleatoria...")
                cancion = random.choice(self.lista_musica)
                duracion = self.obtener_duracion_archivo(cancion)
                return cancion, duracion
    
    def cargar_musica_desde_carpeta(self, carpeta_musica="music"):
        """
        Carga todos los archivos de música desde una carpeta
        """
        if not os.path.exists(carpeta_musica):
            os.makedirs(carpeta_musica)
            print(f"📁 Carpeta '{carpeta_musica}' creada. Coloca tus archivos de música aquí.")
            print("🎵 Formatos soportados: .mp3, .wav, .ogg, .m4a")
            return False
        
        # Buscar archivos de música
        extensiones = ['*.mp3', '*.wav', '*.ogg', '*.m4a']
        self.lista_musica = []
        
        for extension in extensiones:
            archivos = glob.glob(os.path.join(carpeta_musica, extension))
            self.lista_musica.extend(archivos)
        
        if not self.lista_musica:
            print(f"🔍 No se encontraron archivos de música en '{carpeta_musica}'")
            print("🎵 Coloca archivos .mp3, .wav, .ogg o .m4a en la carpeta para escuchar música.")
            return False
        
        print(f"🎵 Encontradas {len(self.lista_musica)} canciones:")
        for cancion in self.lista_musica:
            duracion = self.obtener_duracion_archivo(cancion)
            print(f"   • {os.path.basename(cancion)} ({duracion//60}:{duracion%60:02d})")
        
        return True
    
    def reproducir_musica_seleccionada(self):
        """
        Permite seleccionar y reproducir una canción específica
        """
        if not self.lista_musica:
            return 120  # Duración por defecto
        
        cancion_seleccionada, duracion = self.seleccionar_cancion_interactiva()
        
        if cancion_seleccionada is None:
            return 120
        
        try:
            pygame.mixer.music.load(cancion_seleccionada)
            pygame.mixer.music.set_volume(self.volumen_actual)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.musica_actual = cancion_seleccionada
            self.estado_simulacion = "activa"
            self.duracion_cancion = duracion
            print(f"🎵 Reproduciendo: {os.path.basename(cancion_seleccionada)}")
            print(f"⏱️  Duración de simulación: {duracion//60}:{duracion%60:02d}")
            return duracion
        except Exception as e:
            print(f"❌ Error al reproducir {cancion_seleccionada}: {e}")
            return 120
    
    def cambiar_musica_por_evento(self, tipo_evento):
        """
        Cambia la música basada en eventos de la simulación
        """
        if not self.lista_musica or len(self.lista_musica) <= 1:
            return
        
        # Probabilidad de cambiar música según el evento
        probabilidades = {
            "nueva_conexion": 0.05,  # 5% de cambiar con nueva conexión
            "conexion_rota": 0.08,   # 8% de cambiar cuando se rompe conexión
            "circulo_eliminado": 0.03, # 3% cuando se elimina un círculo
            "muchas_conexiones": 0.15  # 15% cuando hay muchas conexiones activas
        }
        
        if random.random() < probabilidades.get(tipo_evento, 0):
            self.cambiar_cancion()
    
    def cambiar_cancion(self):
        """
        Cambia a una canción diferente con fade
        """
        if not self.lista_musica:
            return
        
        # Seleccionar una canción diferente a la actual
        opciones = [c for c in self.lista_musica if c != self.musica_actual]
        if not opciones:
            return
        
        nueva_cancion = random.choice(opciones)
        
        try:
            # Fade out rápido
            self.fade_out(duracion=1.0)
            
            # Cargar nueva canción
            pygame.mixer.music.load(nueva_cancion)
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.play(-1)
            
            # Fade in
            self.fade_in(duracion=2.0)
            
            self.musica_actual = nueva_cancion
            print(f"🔄 Cambiando a: {os.path.basename(nueva_cancion)}")        
        except Exception as e:
            print(f"❌ Error al cambiar música: {e}")
    
    def iniciar_fade_final(self):
        """
        Marca que la simulación está terminando (sin fade automático)
        """
        self.estado_simulacion = "finalizando"
        print("🎵 Fase final - dejando que la canción termine naturalmente...")
    
    def actualizar_audio(self, tiempo_restante_segundos, num_conexiones=0):
        """
        Actualiza el estado del audio cada frame (sin fade automático)
        """
        if not pygame.mixer.music.get_busy():
            return
        
        # Volumen dinámico basado solo en conexiones (sin fade temporal)
        factor_conexiones = min(1.0, 0.3 + (num_conexiones * 0.02))
        self.volumen_actual = self.volumen_base * factor_conexiones
        
        pygame.mixer.music.set_volume(max(0, min(1, self.volumen_actual)))
    
    def fade_out(self, duracion=2.0):
        """
        Fade out gradual
        """
        pygame.mixer.music.fadeout(int(duracion * 1000))
    
    def fade_in(self, duracion=2.0):
        """
        Fade in gradual (simulado)
        """
        # Pygame no tiene fade_in directo para music, lo simulamos
        pasos = int(duracion * 60)  # 60 FPS
        volumen_paso = self.volumen_base / pasos
        
        for i in range(pasos):
            pygame.mixer.music.set_volume(volumen_paso * i)
            pygame.time.wait(int(1000/60))
    
    def detener_audio(self):
        """
        Detiene toda la música
        """
        pygame.mixer.music.stop()
        print("🔇 Audio detenido")

# Función de conveniencia para crear una instancia global
gestor_audio = GestorAudio()
