import ConfigParser

class ConfigReader:

	DEFAULT_SLEEP_TIME = 5
	DEFAULT_MAX_ERRORS = 12
	DEFAULT_CONNECTION_TIMEOUT = 2

	RECEIVERS_DELIMITER = ","
	DEFAULT_YO_LINK = "http://pedrorijo91.github.io/"

	DEFAULT_EMAIL_SUBJECT = "Lighthouse Keeper - Website down "
	DEFAULT_EMAIL_BODY = "The website you've subscribed through Lighthouse Keeper is down.\n Check https://github.com/pedrorijo91/lighthouse-keeper"

	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		self.config.read("config.ini")

	def read_url(self):
		return self.config.get('host', 'url')

	def read_token(self):
		return self.config.get('yo', 'token')

	def read_sleep_time(self): #seconds
		if self.config.has_option('time', 'sleep_time'):
			return self.config.getfloat('time', 'sleep_time')
		else:
			return DEFAULT_TIME_SLEEP

	def read_max_errors(self):
		if self.config.has_option('time', 'max_errors'):
			return self.config.getint('time', 'max_errors')
		else:
			return DEFAULT_MAX_ERRORS

	def read_connection_timeout(self): #seconds
		if self.config.has_option('time', 'connection_timeout'):
			return self.config.getfloat('time', 'connection_timeout')
		else:
			return DEFAULT_CONNECTION_TIMEOUT

	def read_yo_receivers(self):
		if self.config.has_option('yo', 'receivers'):
			return self.config.get('yo', 'receivers').split(self.RECEIVERS_DELIMITER)
		else:
			return []

	def read_yo_link(self):
		if self.config.has_option('yo', 'link'):
			return self.config.get('yo', 'link')
		else:
			return DEFAULT_YO_LINK

	def read_email_server(self):
		return self.config.get('email', 'server')	

	def read_email_account(self):
		return self.config.get('email', 'account')

	def read_email_password(self):
		return self.config.get('email', 'password')

	def read_email_dest(self):
		if self.config.has_option('email', 'recipients'):
			return self.config.get('email', 'recipients').split(self.RECEIVERS_DELIMITER)
		else:
			return [read_email_account]

	def read_email_subject(self):
		if self.config.has_option('email', 'subject'):
			return self.config.get('email', 'subject')
		else:
			return DEFAULT_EMAIL_SUBJECT + read_url()

	def read_email_body(self):
		if self.config.has_option('email', 'body'):
			return self.config.get('email', 'body')
		else:
			return DEFAULT_EMAIL_BODY

