

import os
import uuid

import httpx
import pytest


log_dir = './'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


class TestGoAccessAPI:
    BASE_URL = "https://goaccess.orange.local/"

    @pytest.fixture
    def client(self):
        """Create HTTPX client for testing"""
        with httpx.Client(base_url=self.BASE_URL,verify=False, timeout=30.0) as client:
            yield client

    @pytest.fixture
    def sample_log_data(self):
        """Sample log data for testing upload"""
        log_file = f"{os.path.dirname(os.path.realpath(__file__))}/logs/test.combined.log"
        with open(log_file ,'r',encoding='utf-8') as file:
            return file.read()


    def test_upload_log_file(self, client, sample_log_data):
        """Test uploading a log file"""
        __test__ = False
        response = client.post(
            "/upload",
            content=sample_log_data,
            headers={"Content-Type": "text/plain"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "OK"
        assert "report" in data

        # Extract file_id from the report URL for use in other tests
        report_url = data["report"]
        file_id = report_url.split("/")[-1]

        return file_id


    def test_generate_report(self, client, sample_log_data):
        """Test generating a report from uploaded log file"""

        # First upload a file
        file_id = self.test_upload_log_file(client, sample_log_data)

        # Then generate report
        response = client.get(f"/api/generate/{file_id}")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"

        # Check that response contains HTML content
        html_content = response.text
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content

    def test_generate_report_with_parameters(self, client, sample_log_data):
        """Test generating report with query parameters"""

        file_id = self.test_upload_log_file(client, sample_log_data)
        params={
            "mth": "GET",  # Filter by GET method
            "fmt": "combined"  # Use combined log format
        }

        response = client.get(
            f"/api/generate/{file_id}?mth={params['mth']}&fmt={params['fmt']}"
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"

    def test_generate_report_invalid_file_id(self, client):

        """Test generating report with invalid file ID"""
        invalid_file_id = str(uuid.uuid4())  # Random UUID that shouldn't exist

        response = client.get(f"/api/generate/{invalid_file_id}")

        # The API might return 404 or 400 for invalid file IDs
        assert response.status_code in [400, 404, 500]

    def test_upload_empty_file(self, client):

        """Test uploading an empty log file"""
        response = client.post(
            "/upload",
            content="",
            headers={"Content-Type": "text/plain"}
        )

        # API might handle empty files differently
        assert response.status_code in [200, 400]


# Example of running tests sequentially
if __name__ == "__main__":
    # This is a simple way to run the tests without pytest
    api_test = TestGoAccessAPI()


#    with httpx.Client(base_url=api_test.BASE_URL, timeout=30.0) as client:
        # Test upload
        #sample_data  = api_test.sample_log_data()

#        try:
#            file_id = api_test.test_upload_log_file(client, sample_data)
#            print(f"✓ Upload test passed. File ID: {file_id}")
#
#            # Test generate
#            api_test.test_generate_report(client, sample_data)
#            print("✓ Generate report test passed")
#
#            # Test download
#            api_test.test_download_report(client, sample_data)
#            print("✓ Download report test passed")
#
#            print("All tests passed!")

#        except Exception as e:
#            print(f"Test failed: {repr(e)}")


