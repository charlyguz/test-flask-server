import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from dotenv import load_dotenv
import time
#import openai
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Configurar la clave de API de OpenAI
#openai.api_key = os.getenv('OPENAI_API_KEY')

# Nuevas funciones basadas en el contexto del audio
def analyze_finances():
    pass  # Aquí iría la lógica para analizar finanzas

def make_transaction():
    pass  # Aquí iría la lógica para hacer una transacción

# Función de prueba para verificar que está funcionando
def test_function():
    testing_message = "Esta es una función de prueba todo está funcionando correctamente."
    print(testing_message)
    #speak_text(testing_message)
    return testing_message







# Función para transcribir voz a texto usando la API de OpenAI Whisper
def transcribe_speech_to_text_with_whisper(file_path):
    
     

    try:
        # Transcribir el audio usando la API de OpenAI Whisper
        with open(file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        text = response.text
        print(f"Texto reconocido: {text}")
        return text
    except Exception as e:
        print(f"Error en la transcripción de Whisper: {e}")
        return ""
   



# Función para transcribir voz a texto usando la API de OpenAI Whisper
def transcribe_speech_to_text(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)  # Leer todo el archivo de audio
            # Puedes ajustar el idioma según tus necesidades, por ejemplo, 'es-ES' para español de España
            transcription = recognizer.recognize_google(audio, language='es-419')
            print(f'Transcripción: {transcription}')
            return transcription
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
        return "No se pudo entender el audio."
    except sr.RequestError as e:
        print(f"Error al comunicarse con el servicio de reconocimiento de voz; {e}")
        return f"Error de reconocimiento de voz: {e}"
    except Exception as e:
        print(f"Ocurrió un error durante la transcripción: {e}")
        return f"Error durante la transcripción: {e}"


def confirmation(prompt, model="gpt-4o-mini"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Quiero que entiendas el contexto de la respuesta y me respondas únicamente con 'si' o 'no', dependiendo de si la respuesta del usuario es afirmativa o negativa. No tienes permitido responder con ninguna otra palabra que no sea 'si' o 'no'. Analiza el contexto de lo que dice el usuario y responde de acuerdo con el contexto. La pregunta que se le ha hecho al usuario puede ser algo como: '¿La información es correcta?' o '¿Desea continuar?'. Tu tarea es determinar si la respuesta es afirmativa o negativa y responder solo con 'si' o 'no'. Tu respuesta final no debe contener puntos, comas, acentos ni ninguna otra puntuación, solo debe ser la palabra 'si' o 'no' tal y como están escritas en este mensaje."},
                {"role": "user", "content": prompt}
            ],
        )
        print(response.choices[0].message.content)
        if response.choices[0].message.content.lower() == "si":
            return True
        return False
    except Exception as e:
        print(e)
        return False

def get_gpt_response(prompt, model="gpt-4"):
    functions = {
        "analizar_finanzas": analyze_finances,
        "hacer_transaccion": make_transaction,
        "funcion_prueba": test_function
    }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente servicial. Para cada solicitud, responde con la acción a realizar como primera palabra. Las acciones disponibles son: 'analizar_finanzas', 'hacer_transaccion', y 'funcion_prueba'. Tu respuesta no debe contener puntos, comas, acentos ni ninguna otra puntuación. Las respuestas deben ser concisas y brindar un excelente servicio al cliente. Termina cada respuesta con 'seguiremos con los siguientes pasos'. No proporciones los pasos detallados para la acción. Ten en cuenta que realizar un depósito significa que quieres hacer una transacción."},
                {"role": "user", "content": prompt}
            ],
        )
        # Obtener el texto de la respuesta de ChatGPT
        res = response.choices[0].message.content
        #print(f"Respuesta de ChatGPT: {res}")

        # Obtener la acción de la respuesta (primera palabra)
        action = res.split(" ")[0].lower()
        print(f"Acción: {action}")
        print(f"Respuesta completa de ChatGPT: {res}")
        #speak_text(res)
        
        if action in functions:
            function = functions[action]
            print(f"Llamando a la función: {function.__name__}")
            function()  # Llamar a la función correspondiente
        else:
            print("No se encontró una acción válida en la respuesta de ChatGPT")
            
        return res
    except Exception as e:
        print(e)
        return f"Error al obtener respuesta de ChatGPT: {e}"

def speak_text(text):
    try:
        tts = gTTS(text=text, lang='es-mx')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
    except Exception as e:
        print(f"Error al reproducir el texto: {e}")

def start_interaction():
    try:
        while True:
            print("Iniciando reconocimiento de voz...")
            #speak_text("Hola, ¿en qué puedo ayudarte?")
            #user_input = transcribe_speech_to_text()
            


            #user_input = transcribe_speech_to_text_with_whisper("audio.wav")
            user_input = "Hola, esta es una prueba asi que llama a la funcion de prueba"
            if not user_input:
                speak_text("No entendí lo que dijiste. Por favor, inténtalo de nuevo.")
                continue  # Reinicia el ciclo sin llamar a la función nuevamente

            print("Obteniendo respuesta de ChatGPT...")
            gpt_response = get_gpt_response(user_input)
            #print(f"Respuesta de ChatGPT: {gpt_response}")
            #speak_text(gpt_response)

            print("Todo bien hasta aqui, finalizando interacción prueba")
            break
            
            speak_text("¿Desea realizar otra operación?")
            user_confirmation = transcribe_speech_to_text()
            if not confirmation(user_confirmation):
                speak_text("Hasta luego, que tenga un buen día")
                break  # Sale del ciclo y finaliza la función
    except Exception as e:
        print(f"Ocurrió un error en la interacción: {e}")
        speak_text("Ocurrió un error inesperado. Por favor, reinicia la interacción.")
