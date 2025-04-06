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

banner = Colorate.Vertical(Colors.red_to_yellow, Center.Center(bannerText), 1)
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
REPORT_REASON = int(Write.Input("Enter the violation type ID: ", Colors.red_to_yellow, interval=0.0025))
REPORT_DESCRIPTION = Write.Input("Enter the report description: ", Colors.red_to_yellow, interval=0.0025)
NUM_REPORTS = int(Write.Input("Enter the number of reports to send: ", Colors.red_to_yellow, interval=0.0025))
REPORT_INTERVAL = float(Write.Input("Enter the time in seconds between reports (e.g., 0.5): ", Colors.red_to_yellow, interval=0.0025))

# Cookie input choice
cookie_choice = Write.Input("Enter '1' to use a specific cookie, or '2' to use a random cookie from cookies.txt: ", Colors.red_to_yellow, interval=0.0025)

if cookie_choice == "1":
    cookie = Write.Input("Enter the .ROBLOSECURITY cookie: ", Colors.red_to_yellow, interval=0.0025)
    cookies = [9AA8C9D7301709D5AA9EC05117E0AE156080DA7950514F6B7F8FEB29DA6965808A5B506C67A96BA8ABD863D50279B4815F02FCA5A79145A6DE501845EF670A1D87C34A508BBF32C62ED195DD7E9B6550193B22DCB6C4F5AA7A2068B127EE6E59603B3A2086E0C80A459CD6C2055D6A3723BF51C30B18871EA479E03E662FF09D74998D2C8FE957B8DD4653C0073CEF99FD55D7777783AEA5B84BF3E85BC5FD21F03C49DCE70B320446FD5A936287F7F0ADFB88C541A832866BA347B25F3C39C6A89398C236402718921C8B0A0BCD9F996818532EB322FFEB5C23033917F35A119D9C7D7D30BF830A6293B198E429FA7046691F0B994C445D8CBA57BA3E8C65DEA2A967F87EE943E31D870E0D29D4F8B7F8AAEF80792C11BB4BCD1CD3157C0912EEBA77458B8207FCEB07B1B552C666F63513E9C5B1C3896C99EF712C575A46E29AA2537B2A32C42229538588C5314088B688ECA51981141E6DD7C450E84D5F1A4A3E974F8E3C263B76FC41F1239FD3829444B5CE1D99E600E536F08B3F241E8E84E2A52E122F7CDB9EC544C5581CBFB1A14E4E64291629A12AB15C97036B09E0B3A53234D45DC6646B838B6DCB5D514F958E693FA4945F8575D3EDDC65B0817AF3324B4D385E0612E73749BAB526F0048726C6A57C5A235525AAE79B492603A573C4298D5C5A41594E5B7C4EF9677DBE7A0BF5B605B74D451C189099E9B66139235A6D35DBCE8ECB980C756D297D6D6D1F73A9166CE6AEF9DBA0CAA07E17183C134ECBE4637FE4D476D9C2B9316EBF48030534352E2A92A87B7992AB06DFE00CCD16C41E0B2329FC220C6B5B897588546EF26635B017457E011FEF894732E862878B4B6AA8D9C4529E223B17E8F7D8332A41CADA18CB3FB7D8EC73CD83AC67725AB0D0A220CF1165EDDD8D86C7F5A509629878F59265CEE93EF8CA393F761A2E7165518A872F12EFCFB2C2B9FB344F95AC0B86B0193DD65FB85A847B8C2B37DFC6FF3A330682E00C63079B5F2D1C1384AC727979FFF5CDCD7708039C1230E699CB9C199F1907C83103D73BB3113B98E8BA0F572773E252C69A59D5CAE89C1549D200C5ABC6C5CDC9547795AFBD4374659CD1ECE53A64846F1EA819154CE5447C73ADFC49]
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
