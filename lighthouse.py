import httplib
import time
import socket
import logging
import smtplib
import sys
sys.path.append("YoPy")
import yopy
import configReader

config = configReader.ConfigReader()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def ping():
	'''
	if you want to simulate some errors you may try returning one of the following:
	-> raise socket.timeout
	-> return 404,"lol"
	'''
	conn = httplib.HTTPConnection(config.read_url(), timeout=config.read_connection_timeout())
	conn.request("HEAD", "/")
	ping = conn.getresponse()
	return ping.status, ping.reason

def is_server_ok(status):
	return status < 400

def deal_error(counter, down, message):
	logging.warning(message)
	counter += 1

	if counter >= config.read_max_errors() and not down:
		down = True
		notify()

	time.sleep(config.read_sleep_time())

	return down

def notify_yo():
	token = config.read_token()
	yo = yopy.Yo(token)

	receivers = config.read_yo_receivers()
	link = config.read_yo_link()

	if not receivers:
		logging.info("yo to all  with link: " + link)
		yo.yoall(link)
	else:
		for receiver in receivers:
			logging.info("yo to " + receiver + " with link: " + link)
			yo.youser(receiver, link)

def notify_email():
	username = config.read_email_account()
	password = config.read_email_password()

	fromaddr = username
	toaddrs = config.read_email_dest()
	msg = "\r\n".join([
	  "From: " + fromaddr,
	  "To: " + str(toaddrs),
	  "Subject: " + config.read_email_subject(),
	  "",
	  config.read_email_body()
	  ])

	logging.info("emailing: " + str(toaddrs))

	server = smtplib.SMTP(config.read_email_server())
	server.starttls()
	server.login(username, password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

def notify():
	logging.error("notifying")
	notify_yo()
	notify_email()

def main():
	counter = 0
	down = False

	while True:
		try:
			status, reason = ping()

			if is_server_ok(status):
				logging.info("success: " + str(status) + " " + reason)
				counter = 0
				time.sleep(config.read_sleep_time())
				down = False
			else:
				counter += 1
				down = deal_error(counter, down, "failed: " + str(status) + " " + reason)

		except socket.timeout:
			counter += 1
			down = deal_error(counter, down, "failed: socket.timeout exception")

main()
