# """
# Unit tests for the app config token rotation logic
# """
# import unittest
# from pydantic import SecretStr
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv, find_dotenv, dotenv_values
#
# from slack_bot.token_rotation import rotate_token
#
# dotenv_path = find_dotenv()
# load_dotenv(dotenv_path)
# env_values = dotenv_values(dotenv_path)
#
#
# class Settings(BaseSettings):
#     """Environment variables settings"""
#     access_token: SecretStr
#     signing_secret: SecretStr
#     config_data_dir: str = './config_data/'
#     app_config_token: SecretStr = SecretStr('')
#     bot_app_id: str = ''
#     refresh_token: SecretStr = SecretStr('')
#
#     class Config:
#         env_file = '.env'
#         env_prefix = 'slack_'
#         case_sensitive = False
#
#
# class TestRotateToken(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.test_settings = Settings(
#             access_token=SecretStr(env_values['SLACK_ACCESS_TOKEN']),
#             signing_secret=SecretStr(env_values['SLACK_SIGNING_SECRET']),
#             config_data_dir=env_values['SLACK_CONFIG_DATA_DIR'],
#             app_config_token=SecretStr(env_values['SLACK_APP_CONFIG_TOKEN']),
#             bot_app_id=env_values['SLACK_BOT_APP_ID'],
#             refresh_token=SecretStr(env_values['SLACK_REFRESH_TOKEN'])
#         )
#         self.copy_settings = self.test_settings.model_copy()
#
#     def test_rotate_token_success(self):
#         # Call the rotate_token function with the test settings
#         result = rotate_token(self.test_settings)
#
#         # Assert that the function returns a tuple with two values
#         self.assertIsInstance(result, tuple)
#         self.assertEqual(len(result), 2)
#
#         # Assert that test settings have changed, while the original's copy has not
#         self.assertEqual(self.test_settings.refresh_token.get_secret_value(), result[1])
#         self.assertEqual(self.test_settings.app_config_token.get_secret_value(), result[0])
#         self.assertNotEqual(self.copy_settings.refresh_token.get_secret_value(), result[1])
#         self.assertNotEqual(self.copy_settings.app_config_token.get_secret_value(), result[0])
#
#     def test_rotate_token_failure(self):
#         # Call the rotate_token function with the test settings
#         self.test_settings.refresh_token = SecretStr('failed_token')
#         self.copy_settings.refresh_token = SecretStr('failed_token')
#         result = rotate_token(self.test_settings)
#
#         # Assert that the function returns an empty tuple
#         self.assertEqual(result, ())
#
#         # Assert that copy and test token stay the same
#         self.assertEqual(self.copy_settings.refresh_token.get_secret_value(),
#                          self.test_settings.refresh_token.get_secret_value())
#         self.assertEqual(self.copy_settings.app_config_token.get_secret_value(),
#                          self.test_settings.app_config_token.get_secret_value())
#
#
# if __name__ == '__main__':
#     unittest.main()
