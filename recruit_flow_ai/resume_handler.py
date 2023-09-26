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
    def __init__(self):
        self.s3 = s3()

    def download_pdf(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Extract the file name from the URL
            filename = os.path.basename(url)

            with open(filename, 'wb') as f:
                f.write(response.content)

            logging.info(f"Downloaded PDF and saved as {filename}")
            return filename
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading PDF: {e}")
            return None

    def parse_pdf(self, pdf_file):
        pass

    def upload_pdf_to_minio(self, pdf_file_path):
        try:
            # Check if file exists
            if not os.path.exists(pdf_file_path):
                logging.error(f"File {pdf_file_path} does not exist.")
                return None

            # Check if file is a PDF
            if not pdf_file_path.endswith('.pdf'):
                logging.error(f"File {pdf_file_path} is not a PDF.")
                return None

            return self.s3.upload_pdf(pdf_file_path)
        except Exception as e:
            logging.error(f"Error uploading to Minio: {e}")
    
    def save_resume(self, url):
        # Download the PDF
        pdf_file = self.download_pdf(url)
        if pdf_file is None:
            return None

        # Upload the PDF to Minio
        minio_url = self.upload_pdf_to_minio(pdf_file)
        if minio_url is None:
            return None

        # Delete the temporary file
        try:
            os.remove(pdf_file)
            logging.info(f"Deleted temporary file {pdf_file}")
        except Exception as e:
            logging.error(f"Error deleting temporary file {pdf_file}: {e}")

        return minio_url