from django.test import TestCase

# Create your tests here.
import datetime
# date = datetime.datetime.now()
# date = input('>>')
# print(len(str(date)))
import fernet
f = fernet.Encrypter('salom')
print(f)