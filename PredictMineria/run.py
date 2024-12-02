from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar el archivo .env

app = create_app()

if __name__ == '__main__':
    cert_path = os.getenv('SSL_CERTFILE')
    key_path = os.getenv('SSL_KEYFILE')
    port = os.getenv('PORT')
    
    # Si no los encuentra, lo hace sobre HTTP por defecto
    if cert_path and key_path:
        app.run(debug=True, host='0.0.0.0', port=int(port), ssl_context=(cert_path, key_path))
    else:
        print("Los archivos de certificado no se encontraron. Usando HTTP en su lugar.")
        app.run(debug=True, host='0.0.0.0', port=4006)
