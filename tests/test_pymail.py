# Testers should declare `config_path' before running this test

from unittest import TestCase, main as RunUnitTest
from pymail.smtp import PyMail
from email.mime.text import MIMEText

class PyMailTest(TestCase):
	def test_object_construction(result):
		mail = PyMail(config_path = config_path)
	
	def test_smtp_connect(result):
		mail = PyMail(config_path = config_path)
		connection = mail.Connect()
		connection.quit()
	
	def test_send_email(result):
		msg = MIMEText('LibPyMail test_send_email payload')
		msg['Subject'] = 'LibPyMail test_send_email'
		msg['To'] = 'robertbeam@gmail.com'
		
		mail = PyMail(config_path = config_path)
		connection = mail.Connect()
		connection.send_message(msg)
		#connection.quit()

if __name__ == "__main__":
	RunUnitTest()