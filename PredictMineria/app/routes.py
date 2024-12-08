from flask import Blueprint, request, jsonify
from app.services import get_user_data, predict_next_day, save_user_data

api = Blueprint('api', __name__)

@api.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener datos del body de la solicitud
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id es requerido en el body de la solicitud"}), 400

        # Obtener datos del usuario
        df = get_user_data(user_id)

        # Validar si hay suficientes registros
        if len(df) < 30:
            return jsonify({"error": "El usuario no tiene al menos 30 registros para realizar la predicción"}), 400

        # Realizar predicción
        response_data = predict_next_day(df)

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/save', methods=['POST'])
def save():
    try:
        # Obtener datos del body de la solicitud
        data = request.get_json()
        user_id = data.get('user_id')
        minutes = data.get('minutes')
        date = data.get('date')

        if not user_id or not minutes or not date:
            return jsonify({"error": "user_id, minutes, y date son requeridos"}), 400

        # Guardar los datos del usuario en MongoDB
        save_user_data(user_id, minutes, date)

        return jsonify({"message": "Datos guardados exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500