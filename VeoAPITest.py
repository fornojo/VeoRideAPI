import requests
import time

host = "manhattan-host.veoride.com"
port = 8444

def request_verification_code(phonenumber):

    loginurl = f"https://{host}:{port}/api/auth/customers/{phonenumber}/verification_code"

    result = requests.get(loginurl)

    return result

def verify_code(phonenumber, code, phoneModel="iPad Air 2"):
    appversion = "2.2.1"
    verifyurl = f"https://{host}:{port}/api/auth/customers/verify_code"
    body = {
        "phone": phonenumber,
        "phoneModel": phoneModel,
        "appVersion": appversion,
        "code": code,
    }
    result = requests.post(verifyurl, json=body)
    return result

def bikes_nearby(accesstoken, lat, lng):
    nearbyurl = f"https://{host}:{port}/api/customers/vehicles?lat={lat}&lng={lng}"
    headers = {
        "Authorization": token
    }

    result = requests.get(nearbyurl, headers=headers)
    return result

phone = input("What is the phone number? ")
result = request_verification_code(phone)
code = input("What is the verification code? ")
result = verify_code(phone, code)
json = result.json()
if result.status_code != 200:
    print ("failure!")
    exit()
token = json['data']['jwtAuthentication']['tokenType'] + ' ' + json['data']['jwtAuthentication']['accessToken']

bikesmap = {}
try:
    lat = float(input("What is your latitude? [40.1019564, -88.2293502] "))
    lon = float(input("What is your longitude? [40.1019564, -88.2293502] "))
except:
    lat, lon = 40.1019564,-88.2293502
print("loc:")
print (lat)
print(lon)
while True:
    result = bikes_nearby(token, lat, lon)
    if result.status_code != 200:
        print("Failed to fetch nearby!")
        exit()
    json = result.json()
    list = json['data']
    for bike in list:
        if bike['vehicleNumber'] in bikesmap:
            # check if lock status or location has changed
            existing = bikesmap[bike['vehicleNumber']]
            if existing['lockStatus'] != bike['lockStatus']:
                print(f"{bike['vehicleNumber']} lock status changed from {existing['lockStatus']} to {bike['lockStatus']}.")
            if existing['location']['lat'] != bike['location']['lat'] or existing['location']['lng'] != bike['location']['lng']:
                print(f"{bike['vehicleNumber']} location changed from {existing['location']['lat']}, {existing['location']['lng']} to {bike['location']['lat']}, {bike['location']['lng']}.")

        else:
            print(f"Now monitoring {bike['vehicleNumber']}; lock status: {bike['lockStatus']}; location: {bike['location']['lat']}, {bike['location']['lng']}")
        bikesmap[bike['vehicleNumber']] = bike
    time.sleep(5)