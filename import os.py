import os
import yt_dlp
import threading
import imageio_ffmpeg  
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

class YTMusicDonwloader(App):
    def build(self):
        ventana = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.texto_titulo = Label(text="MÚSICA 67 🎶", font_size='24sp', bold=True)
        ventana.add_widget(self.texto_titulo)

        self.caja_enlace = TextInput(hint_text="Pega el link de YouTube o Mix aquí...", multiline=False)
        ventana.add_widget(self.caja_enlace)

        self.boton = Button(text="DESCARGAR MP3 🚀", background_color=(0.2, 0.5, 1, 1), font_size='18sp')
        self.boton.bind(on_press=self.iniciar_hilo_descarga)
        ventana.add_widget(self.boton)

        self.texto_estado = Label(text="Esperando tu canción...")
        ventana.add_widget(self.texto_estado)

        return ventana

    def iniciar_hilo_descarga(self, instance):
        url_original = self.caja_enlace.text.strip()

        if not url_original:
            self.texto_estado.text = "¡Olvidaste pegar el enlace ❌"
            return

        # Cortamos el enlace del Mix para descargar solo la canción actual
        if "&list=" in url_original:
            url_youtube = url_original.split("&list=")[0]
        elif "?list=" in url_original:
            url_youtube = url_original.split("?list=")[0]
        else:
            url_youtube = url_original

        self.texto_estado.text = "Descargando tu canción... Por favor espera ⏳"
        
        hilo = threading.Thread(target=self.procesar_musica, args=(url_youtube,))
        hilo.start()

    def procesar_musica(self, url_youtube):
        # CARPETA DE DESCARGAS EXCLUSIVA PARA EL CELULAR DE MAMÁ
        ruta_guardar = "/sdcard/Download"
        
        if not os.path.exists(ruta_guardar):
            # CARPETA DE DESCARGAS EXCLUSIVA PARA TU PC WINDOWS
            ruta_guardar = os.path.join(os.path.expanduser("~"), "Downloads")

        ajustes = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(ruta_guardar, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': True,  
            'no_warnings': True,
            'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),  
            'noplaylist': True,  
            
            'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
            
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ajustes) as ydl:
                ydl.download([url_youtube])
            Clock.schedule_once(lambda dt: self.finalizar_descarga(exito=True))
        except Exception as e:
            print(f"Error: {e}")
            Clock.schedule_once(lambda dt: self.finalizar_descarga(exito=False))

    def finalizar_descarga(self, exito):
        if exito:
            self.texto_estado.text = "¡Listo! Canción guardada en Descargas. 🎉"
            self.caja_enlace.text = ""  
        else:
            self.texto_estado.text = "Error al descargar. Intenta con otro video."

if __name__ == "__main__":
    YTMusicDonwloader().run()
