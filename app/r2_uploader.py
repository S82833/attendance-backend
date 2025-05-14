import boto3
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from botocore.config import Config
from datetime import timedelta

load_dotenv()

ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
REGION = "us-east-1"

# Endpoint de R2 (formato específico)
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"

# Cliente S3 compatible con R2
s3 = boto3.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version='s3v4'),
)

def upload_image_to_r2(image, uid, timestamp):
    try:
        if not image or not image.file:
            raise ValueError("Archivo vacío o no válido")

        filename = f"{uid}_{timestamp.strftime('%Y%m%d%H%M%S')}.jpg"

        # 🔄 Volver al inicio del archivo (importante)
        image.file.seek(0)

        # 🧪 PROBAMOS LEER PRIMERO
        image.file.seek(0)

        # 🔼 Subir a R2
        s3.upload_fileobj(image.file, BUCKET_NAME, filename)

        url = f"https://imagenes.asistenciapcte.com/{filename}"
        print("✅ Imagen subida, URL generado:", url)
        return url

    except Exception as e:
        print("❌ Error subiendo imagen:", e)
        raise




