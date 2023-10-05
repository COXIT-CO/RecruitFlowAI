"""
This module contains a class for handling PDF files. It includes methods for 
downloading a PDF from a URL, parsing a PDF file, and uploading a PDF to a 
Minio bucket.
"""
import requests
import os
import logging

from recruit_flow_ai.s3client import S3StorageManager as s3

class ResumeHandler:
    """
    A class for handling PDF files.
    """
    def __init__(self):
        self.s3 = s3()

    def download_pdf(self, url, token=None):
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = requests.get(url, headers=headers, verify=False, timeout=5)
            response.raise_for_status()

            if response.status_code != 200:
                logging.error("Error downloading PDF: Status code %s", response.status_code)
                return None

            filename = os.path.basename(url)

            with open(filename, "wb") as f:
                f.write(response.content)

            logging.info("Downloaded PDF and saved as %s", filename)
            return filename
        except requests.exceptions.RequestException as e:
            logging.error("Error downloading PDF: %s", e)
            return None

    def parse_pdf(self, pdf_file):
        pass

    def upload_pdf_to_minio(self, pdf_file_path):
        try:
            if not os.path.exists(pdf_file_path):
                logging.error("File %s does not exist.", pdf_file_path)
                return None

            if not pdf_file_path.endswith(".pdf"):
                logging.error("File %s is not a PDF.", pdf_file_path)
                return None

            return self.s3.upload_pdf(pdf_file_path)
        except requests.exceptions.RequestException as e:
            logging.error("Error uploading to Minio: %s", e)

    def save_resume(self, url, token=None):
        pdf_file = self.download_pdf(url, token)
        if pdf_file is None:
            return None

        minio_url = self.upload_pdf_to_minio(pdf_file)
        if minio_url is None:
            return None

        try:
            os.remove(pdf_file)
            logging.info("Deleted temporary file %s", pdf_file)
        except OSError as e:
            logging.error("Error deleting temporary file %s: %s", pdf_file, e)

        return minio_url
