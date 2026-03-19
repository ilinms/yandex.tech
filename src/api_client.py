import requests
from config import DISK_BASE_URL


class YandexDiskClient:
    def __init__(self, oauth_token: str):
        self.token = oauth_token
        self.base_url = DISK_BASE_URL

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"OAuth {self.token}",
            "Content-Type": "application/json"
        })

    def get_disk_info(self):
        response = self.session.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def get_resources(self, path: str = "/"):
        response = self.session.get(
            f"{self.base_url}/resources",
            params={"path": path},
        )
        response.raise_for_status()
        return response.json()

    def get_upload_url(self, path: str, overwrite: bool = False) -> str:
        response = self.session.get(
            f"{self.base_url}/resources/upload",
            params={"path": path, "overwrite": str(overwrite).lower()},
        )
        response.raise_for_status()
        return response.json().get("href")

    def get_download_url(self, path: str) -> str:
        response = self.session.get(
            f"{self.base_url}/resources/download",
            params={"path": path},
        )
        response.raise_for_status()
        return response.json().get("href")

    def create_folder(self, path: str):
        response = self.session.put(
            f"{self.base_url}/resources",
            params={"path": path},
        )
        return response

    def copy_resource(self, from_path: str, to_path: str):
        response = self.session.post(
            f"{self.base_url}/resources/copy",
            params={"from": from_path, "path": to_path},
        )
        return response

    def move_resource(self, from_path: str, to_path: str):
        response = self.session.post(
            f"{self.base_url}/resources/move",
            params={"from": from_path, "path": to_path},
        )
        return response

    def delete_resource(self, path: str, permanently: bool = False):
        response = self.session.delete(
            f"{self.base_url}/resources",
            params={"path": path, "permanently": str(permanently).lower()},
        )
        return response

    @staticmethod
    def upload_file(upload_url: str, file_content: bytes) -> requests.Response:
        response = requests.put(upload_url, data=file_content)
        response.raise_for_status()
        return response

    def publish_resource(self, path: str):
        """PUT /resources/publish - опубликовать ресурс"""
        response = self.session.put(
            f"{self.base_url}/resources/publish",
            params={"path": path}
        )
        return response

    def unpublish_resource(self, path: str):
        """PUT /resources/unpublish - отменить публикацию ресурса"""
        response = self.session.put(
            f"{self.base_url}/resources/unpublish",
            params={"path": path}
        )
        return response

    def get_public_url(self, path: str) -> str:
        """GET /resources - получить публичную ссылку на ресурс"""
        response = self.session.get(
            f"{self.base_url}/resources",
            params={"path": path}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("public_url", data.get("public_key", ""))
