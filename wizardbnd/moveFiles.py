import os

try:
	os.chmod("/usr/local/nagiosxi/html/config", 511)
except:
	print("Something went wrong")
try:
	os.mkdir("/usr/local/nagiosxi/html/config/uploads")
except:
	print("Folder already exists")
try:
	os.chmod("/usr/local/nagiosxi/html/config/uploads", 511)
except:
	print("Something went wrong")
try:
 	os.popen("cp /usr/local/nagiosxi/html/includes/configwizards/wizardbnd/handle_file_upload.php /usr/local/nagiosxi/html/config/handle_file_upload.php")
except:
	print("Error")


