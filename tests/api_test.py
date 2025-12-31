import os
import uuid

import httpx
import pytest

log_file = [
'test.combined.log',
'test.combined_x_for.log',
'test.hestia.log',
'test.bitrix.log',
]

log_dir = './'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def read_log_data(name):
    """Sample log data for testing upload"""
    log_file = f"{os.path.dirname(os.path.realpath(__file__))}/logs/{name}"
    with open(log_file ,'r',encoding='utf-8') as file:
        return file.read()

class TestGoAccessAPI:
    BASE_URL = "https://goaccess.orange.local/"

    @pytest.fixture
    def client(self):
        """Create HTTPX client for testing"""
        with httpx.Client(base_url=self.BASE_URL,verify=False, timeout=30.0) as client:
            yield client

    @pytest.fixture(scope="module", params=log_file)
    def log_name(self,request):
        return request.param
   
    def test_upload_log_file(self, client, log_name):
        data=read_log_data(log_name)
        __test__ = False
        response = client.post(
            "/upload",
            content=data,
            headers={"Content-Type": "text/plain"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "OK"
        assert "report" in data

        report_url = data["report"]
        file_id = report_url.split("/")[-1]

        return file_id

    def test_generate_report(self, client, log_name):
        """Test generating a report from uploaded log file"""
        file_id = self.test_upload_log_file(client, log_name)

        response = client.get(f"/api/generate/{file_id}")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"

        html_content = response.text
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content

    def test_generate_report_with_parameters(self, client, log_name):
        """Test generating report with query parameters"""
        file_id = self.test_upload_log_file(client, log_name)
        params={
            "mth": "GET",   
            "fmt": "combined"  
        }
        response = client.get(
            f"/api/generate/{file_id}?mth={params['mth']}&fmt={params['fmt']}"
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
    
    def test_generate_invalid_format(self, client):
        """Test generating report with query parameters"""
        file_id = self.test_upload_log_file(client, "test.badformat.log")

        response = client.get(f"/api/generate/{file_id}")

        assert response.status_code == 400
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        
    def test_generate_report_invalid_file_id(self, client):

        """Test generating report with invalid file ID"""
        invalid_file_id = str(uuid.uuid4())   
 
        response = client.get(f"/api/generate/{invalid_file_id}")

        assert response.status_code in [400, 404, 500]

    def test_upload_empty_file(self, client):

        """Test uploading an empty log file"""
        response = client.post(
            "/upload",
            content="",
            headers={"Content-Type": "text/plain"}
        )

        assert response.status_code in [200, 400]

if __name__ == "__main__":
    api_test = TestGoAccessAPI()
    
 
