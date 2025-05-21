from app.config import get_b2_data


def get_b2_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.B2_ENDPOINT,
        aws_access_key_id=settings.B2_ACCESS_KEY,
        aws_secret_access_key=settings.B2_SECRET_KEY,
    )
