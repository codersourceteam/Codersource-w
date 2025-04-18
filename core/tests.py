from django.test import TestCase

# Create your tests here.
import requests

url = input('Enter url: ')
if not url.startswith('http://') or url.startswith('https://'):
    print('Invalid url!')
    exit()
type = input('Enter type POST or GET: ')
c = 1
if type.lower() == 'post':
    
    while True:
        try:
            requests.post(url)
            print(f'{c}-request Success')
            c +=1
        except:
            print(f'{c}-request Error!')
elif type.lower() == 'get':
    while True:
        try:
            requests.get(url)
            print(f'{c}-request Success ')
            c +=1
        except:
            print(f'{c}-request Error!')
else:
    print('Command Error!!')
