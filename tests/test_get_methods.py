import pytest


class TestGetMethods:

    def test_get_disk_info(self, api_client):
        info = api_client.get_disk_info()
        assert "total_space" in info
        assert "used_space" in info
        assert info["total_space"] > 0

    def test_get_resources_root(self, api_client):
        resources = api_client.get_resources(path="/")
        assert "_embedded" in resources
        assert "items" in resources["_embedded"]

    def test_get_test_folder_resources(self, api_client, test_base_folder):
        resources = api_client.get_resources(path=test_base_folder)
        assert "_embedded" in resources
        assert "items" in resources["_embedded"]

    def test_get_upload_url(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=path, overwrite=True)
        assert upload_url is not None
        assert upload_url.startswith("https://")

    def test_get_nonexistent_download_url(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        with pytest.raises(Exception):
            api_client.get_download_url(path=path)
