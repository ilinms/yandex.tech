import pytest


class TestGetMethods:

    def test_get_disk_info(self, api_client):
        info = api_client.get_disk_info()
        assert "total_space" in info
        assert "used_space" in info
        assert info["total_space"] > 0
        assert "system_folders" in info

    def test_get_resources_root(self, api_client):
        resources = api_client.get_resources(path="/")
        assert "_embedded" in resources
        assert "items" in resources["_embedded"]
        assert isinstance(resources["_embedded"]["items"], list)

    def test_get_test_folder_resources(self, api_client, test_base_folder):
        resources = api_client.get_resources(path=test_base_folder)
        assert "_embedded" in resources
        assert "items" in resources["_embedded"]
        assert isinstance(resources["_embedded"]["items"], list)

    def test_get_upload_url(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=path, overwrite=True)
        assert upload_url is not None
        assert upload_url.startswith("https://")

    def test_get_nonexistent_download_url(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        with pytest.raises(Exception):
            api_client.get_download_url(path=path)

    def test_get_file_metadata(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Получение метаданных файла
        metadata = api_client.get_resources(path=file_path)
        assert metadata["type"] == "file"
        assert metadata["name"] == random_filename
        assert "size" in metadata
        assert metadata["size"] > 0
        assert "mime_type" in metadata
        assert "modified" in metadata

    def test_get_folder_metadata(self, api_client, test_base_folder, random_folder_name):
        # Создание папки
        folder_path = f"{test_base_folder}/{random_folder_name}"
        api_client.create_folder(path=folder_path)

        # Получение метаданных папки
        metadata = api_client.get_resources(path=folder_path)
        assert metadata["type"] == "dir"
        assert metadata["name"] == random_folder_name
        assert "_embedded" in metadata
        assert "items" in metadata["_embedded"]

    def test_get_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        with pytest.raises(Exception) as exc_info:
            api_client.get_resources(path=path)
        assert "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()

    def test_get_trash_resources(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка и удаление файла для заполнения корзины
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())
        api_client.delete_resource(path=file_path, permanently=False)

        # Получение информации о корзине
        resources = api_client.get_resources(path=test_base_folder)
        assert "_embedded" in resources

    def test_get_resource_with_invalid_path(self, api_client):
        invalid_path = "/invalid:name"
        with pytest.raises(Exception) as exc_info:
            api_client.get_resources(path=invalid_path)
        error_str = str(exc_info.value).lower()
        assert any(code in error_str for code in ["400", "404", "invalid", "bad request"])

    def test_get_download_url_for_existing_file(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Получение URL для скачивания
        download_url = api_client.get_download_url(path=file_path)
        assert download_url is not None
        assert download_url.startswith("https://")