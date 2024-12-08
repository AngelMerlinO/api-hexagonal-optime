import pandas as pd
from pymongo import MongoClient, errors
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from app.config import MONGO_URI

# Conexión a MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["mineria-optime"]  # Nombre de la base de datos
    collection = db["timestuden"]  # Nombre de la colección
except errors.ConnectionFailure as e:
    raise Exception(f"Error de conexión a MongoDB Atlas: {e}")
except errors.ConfigurationError as e:
    raise Exception(f"Error de configuración de MongoDB: {e}")

def get_user_data(user_id):
    """Obtiene los datos del usuario desde MongoDB."""
    try:
        query = {"user_id": user_id}
        data = list(collection.find(query, {"_id": 0}))
        if not data:
            raise Exception(f"No se encontraron datos para user_id: {user_id}")
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df.last("30D")  # Retornar los últimos 30 días
    except Exception as e:
        raise Exception(f"Error al obtener datos de MongoDB: {e}")

def predict_next_day(df):
    """Realiza la predicción del próximo día."""
    try:
        # Crear y ajustar el modelo Holt-Winters
        model = ExponentialSmoothing(
            df['minutes'],
            trend="add",
            seasonal="add",
            seasonal_periods=7
        ).fit()

        # Predicción para el próximo día
        next_day_prediction = model.forecast(1).iloc[0]

        # Formatear la respuesta
        return {
            "last_30_days": df.reset_index().to_dict(orient="records"),
            "next_day_prediction": round(next_day_prediction, 2)
        }
    except Exception as e:
        raise Exception(f"Error al realizar la predicción: {e}")

def save_user_data(user_id, minutes, date):
    """Guarda los datos del usuario en MongoDB. Si ya existe el registro para esa fecha, suma los minutos."""
    try:
        # Verificar si ya existe un registro para el usuario y la fecha
        existing_record = collection.find_one({"user_id": user_id, "date": date})

        if existing_record:
            # Actualizar los minutos sumando el nuevo registro al existente
            new_minutes = existing_record["minutes"] + minutes
            collection.update_one(
                {"user_id": user_id, "date": date},
                {"$set": {"minutes": new_minutes}}
            )
        else:
            # Crear un nuevo registro si no existe
            collection.insert_one({"user_id": user_id, "minutes": minutes, "date": date})
    except Exception as e:
        raise Exception(f"Error al guardar los datos del usuario: {e}")