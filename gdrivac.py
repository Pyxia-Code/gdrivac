#FINAL TODO: REQUIREMENTS FILE
import requests, argparse, os, json

#Internal Imports
from subscripts.classes import *

def main():
	#CONSTANTS
	COOKIEFILE = 'cookies.json'
	IA = InteractiveAsker()
	IM = Immmunizer()
	CC = CookieChecker()

	#PARSE ARGUMENTS

	parser = argparse.ArgumentParser(description="I NEED A DESCRIPTION")
	#TODO: ADD A DESCRIPTION

	#ALLOW FOR MULTIPLE URLs
	parser.add_argument("-url",nargs='+',type=str,help="Google Drive URL(s) to immunize against.\nMultiple URLs can be specified in succession.")
	parser.add_argument("-files",nargs='+',type=str,help="Files with Drive URL(s) to immunize against.\nMultiple files can be specified in succession.\nSupported Formats:\n*.txt seperated by newlines.TBA")
	
	parser.add_argument("-sid",type=str,help="Specify cookie value for SID")
	parser.add_argument("-ssid",type=str,help="Specify cookie value for SSID")
	parser.add_argument("-hsid",type=str,help="Specify cookie value for HSID")
	parser.add_argument("-tcount",type=int,help="Thread count (recommended = 6)")
	
	args = parser.parse_args()

	#UNPARSE

	files = (args.files or [])
	URLs = (args.url or [])

	for file in files:
		if file[-4:] == '.txt':
			with open(file, 'r') as cookiefile:
				nextline = cookiefile.readline()
				while nextline:
					URLs.append(nextline.strip())
					nextline = cookiefile.readline()

	#COOKIE PAYLOAD
	if not os.path.exists(COOKIEFILE):
		with open(COOKIEFILE, 'w') as cookiefile:
			cookiefile.write('{}')
	
	#Read Cookies
	cookie_payload = {}
	try:
		with open(COOKIEFILE, 'r') as cookiefile:
			cookie_payload = json.load(cookiefile)
	except:
		print("{} is corrupted, resetting cookie payload".format(COOKIEFILE))

	#Update Session Cookies
	if args.sid: cookie_payload['SID'] = args.sid
	if args.ssid: cookie_payload['SSID'] = args.ssid
	if args.hsid: cookie_payload['HSID'] = args.hsid

	#Check and ask interactively for MISSING user session cookies
	if not cookie_payload.get('SID'): cookie_payload['SID']= IA.askFor('SID')
	if not cookie_payload.get('SSID'): cookie_payload['SSID'] =  IA.askFor('SSID')
	if not cookie_payload.get('HSID'): cookie_payload['HSID'] =  IA.askFor('HSID')

	#TODO: Check for cookies shape using CookieChecker CC
	#CC.()

	#Save cookies file
	with open(COOKIEFILE, "w") as cookiefile:
		json.dump(cookie_payload, cookiefile)

	#print(args.sid, args.ssid, args.hsid)
	#print (cookie_payload)

	#GET IMMUNIZED
	if len(URLs):
		IM.request(args,URLs,cookie_payload)
	else:
		print("\033[91mNo URLs provided.\nStopped.\033[0m")

if __name__ == '__main__':
	main()