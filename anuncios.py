#!/usr/bin/python2

#TO TEST HEADERS: www.xhaus.com/headers
import cookielib
import urllib2
import datetime

# Return actual time
def timeStamped(fname = "", fmt = '%d-%m-%Y | %H:%M:%S'):
    return datetime.datetime.now().strftime(fmt).format(fname = fname)

# Auto loggin & auto renew
#
# Login function return 'login' if success.
# Autorenew function return 'pronto' if is too early (1 renew / 24h~~)
#					 return 'renovado' if sucess.
def milanuncios(urlLogin,urlAnuncio):

	request_headers = {"Content-type": "application/x-www-form-urlencoded",
						"Accept": "text/plain",
						"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0"}
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	urllib2.install_opener(opener)
	file = open("log.txt",'a+')

	req1 	 = urllib2.Request(urlLogin, headers=request_headers)
	response = urllib2.urlopen(req1)
	cookie 	 = response.headers.get('Set-Cookie')
	linea 	 = response.read()
	file.write("#######START#######\n")
	file.write(timeStamped())
	file.write("\n" + linea + "\n")

	# Use the cookie in next requests
	req2 	 = urllib2.Request(urlAnuncio, headers=request_headers)
	req2.add_header('Cookie', cookie)
	response = urllib2.urlopen(req2)
	linea 	 = response.read()
	file.write(linea + "\n\n\n")
	file.close()

''' MAIN '''
# 
# Edit it with your info!
#
mail   = "YOUR EMAIL"
passwd = "YOUR PASSWD"

#
# Catch this data with firebug or similar
#
idItem = "YOUR ITEM ID"
idUser = "YOUR USER ID"

urlLogin = "http://www.milanuncios.com/cmd/?comando=login&email=" + mail + "&contra=" + passwd + "&rememberme=s"
urlItem  = "http://www.milanuncios.com/renovado/?comando=renovar&a=a5148ecf1c9f85aadcf0e2feb881df73&t=14bfa6bb14875e45bba028a21ed380466fe262ab722d44a974ce4fc43a8771b1c9f0f895fb98ab9159f51fd0297e236d&u=" + idUser + "&id=" + idItem

# Now, we send the data to the function
milanuncios(urlLogin,urlItem)