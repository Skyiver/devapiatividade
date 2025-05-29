import os
import requests

PESSOA_SERVICE_URL = os.getenv(
    "PESSOA_SERVICE_URL",
    "http://localhost:5002/api/professores"
)

class PessoaServiceClient:
    @staticmethod
    def existe_professor(id_professor: int) -> bool:
        url = f"{PESSOA_SERVICE_URL}/{id_professor}"
        try:
            response = requests.get(url, timeout=3)
            return response.status_code == 200
        except requests.RequestException:
            return False