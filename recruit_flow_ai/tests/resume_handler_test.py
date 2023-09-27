"""
Unit tests for the TestResumeHandler module.
"""
import unittest
from unittest.mock import Mock, patch
import os
from recruit_flow_ai.resume_handler import ResumeHandler 

class TestResumeHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ResumeHandler()

    def test_download_pdf(self):
        handler = ResumeHandler()
        filename = handler.download_pdf('https://cv.coxit.co/cv-pdfs/raphaels-resume.pdf')
        self.assertEqual(filename, "raphaels-resume.pdf")
        self.assertTrue(os.path.exists(filename))

    def test_upload_pdf_to_minio(self):
        handler = ResumeHandler()
        filename = handler.download_pdf('https://cv.coxit.co/cv-pdfs/raphaels-resume.pdf')
        file_path = os.path.join(os.getcwd(), filename)
        s3_file_link = handler.upload_pdf_to_minio(file_path)
        self.assertEqual(f"https://cv.coxit.co/{self.handler.s3.minio_settings.bucket}/{filename}", s3_file_link)


class TestResumeMockedHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ResumeHandler()
        self.handler.s3 = Mock()

    @patch('os.path.exists', return_value=False)
    def test_file_does_not_exist(self, mock_exists):
        result = self.handler.upload_pdf_to_minio('file.pdf')
        self.assertIsNone(result)

    @patch('os.path.exists', return_value=True)
    def test_file_is_not_pdf(self, mock_exists):
        result = self.handler.upload_pdf_to_minio('file.txt')
        self.assertIsNone(result)

    @patch('os.path.exists', return_value=True)
    def test_file_is_pdf_and_exists(self, mock_exists):
        self.handler.s3.upload_pdf.return_value = 'success'
        result = self.handler.upload_pdf_to_minio('file.pdf')
        self.assertEqual(result, 'success')

    @patch('os.path.exists', return_value=True)
    def test_exception_during_upload(self, mock_exists):
        self.handler.s3.upload_pdf.side_effect = Exception('error')
        result = self.handler.upload_pdf_to_minio('file.pdf')
        self.assertIsNone(result)

    @patch('recruit_flow_ai.resume_handler.os.remove')
    @patch.object(ResumeHandler, 'upload_pdf_to_minio')
    @patch.object(ResumeHandler, 'download_pdf')
    def test_save_resume(self, mock_download, mock_upload, mock_remove):
        # Set up the mock methods
        mock_download.return_value = 'test.pdf'
        mock_upload.return_value = 'minio_url'

        # Create a ResumeHandler instance
        handler = ResumeHandler()

        # Call the save_resume method
        result = handler.save_resume('url')

        # Check the result
        self.assertEqual(result, 'minio_url')

        # Check that the mock methods were called correctly
        mock_download.assert_called_once_with('url')
        mock_upload.assert_called_once_with('test.pdf')
        mock_remove.assert_called_once_with('test.pdf')

    

if __name__ == '__main__':
    unittest.main()