import threading
import signal
import os
import sys
from flask import Flask, request, jsonify
from main_logic import start_interaction, transcribe_speech_to_text, transcribe_speech_to_text_with_whisper
from flask_cors import CORS
from werkzeug.utils import secure_filename
#from pydub import AudioSegment


app = Flask(__name__)


# Configurar CORS para permitir solicitudes desde cualquier origen
# Reemplazar '*' con el dominio específico del frontend
CORS(app, resources={r"/*": {"origins": ["*", "http://localhost:5173"]}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'aac', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




# Función para verificar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



'''
# Variables globales para controlar el estado de la interacción
interaction_running = False
interaction_lock = threading.Lock()








# Función para manejar la señal de terminación y cerrar el hilo correctamente
def signal_handler(sig, frame):
    print('Recibida señal de terminación. Cerrando servidor...')
    sys.exit(0)

# Registrar el manejador de señales
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

'''

@app.route('/')
def hello():
    return "¡Hola desde Flask desplegado en Vercel!"

# Ruta opcional para iniciar la interacción manualmente
@app.route('/start_interaction', methods=['POST'])
def start():
    try:
        
        start_interaction()
        return jsonify({'status': 'Interaction started'}), 200
    
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Test successful'}), 200


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No se encontró el archivo de audio en la solicitud.'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No se seleccionó ningún archivo.'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            # Guardar el archivo en el servidor
            file.save(file_path)
            print(f'Archivo guardado en {file_path}')

            # Transcribir el archivo de audio
            transcription = transcribe_speech_to_text_with_whisper(file_path)

            # Opcional: Eliminar el archivo después de procesarlo
            print(f'Archivo {file_path} eliminado después del procesamiento.')
            os.remove(file_path)

            return jsonify({'status': 'success', 'transcription': transcription}), 200

        except Exception as e:
            print(f'Error al procesar el archivo: {e}')
            return jsonify({'status': 'error', 'message': f'Error al procesar el archivo: {str(e)}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Tipo de archivo no permitido.'}), 400



# Función para manejar la señal de terminación y cerrar el hilo correctamente
def signal_handler(sig, frame):
    print('Recibida señal de terminación. Cerrando servidor...')
    sys.exit(0)

# Registrar el manejador de señales
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)



# Adapta la aplicación para que sea manejada por Vercel
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

"""
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)

"""
