from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from cryptography.fernet import Fernet
import json
import base64

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class EncryptedJSONField(models.TextField):
    def get_prep_value(self, value):
        if value is None:
            return value
        json_str = json.dumps(value, cls=DjangoJSONEncoder)
        encrypted_data = cipher_suite.encrypt(json_str.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        encrypted_data = base64.urlsafe_b64decode(value.encode('utf-8'))
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return json.loads(decrypted_data)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            encrypted_data = base64.urlsafe_b64decode(value.encode('utf-8'))
            decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
            return json.loads(decrypted_data)
        return value