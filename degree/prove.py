from django.shortcuts import render , redirect
from . models import Student
from . forms import StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import json
import hashlib
from web3 import Web3

form = StudentForm
name = form.cleaned_data['name']
surname = form.cleaned_data['surname']
birth_date = form.cleaned_data['birth_date']
graduation_date = form.cleaned_data['graduation_date']
grade = form.cleaned_data['grade']
degree = form.cleaned_data['degree']
identifier = form.cleaned_data['identifier']

w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/c6a5a2106678423da4da073723891fc5'))
privateKey = '93c699f6bd96af184c49112ad9876bd469e600603b4351de6cf983fd82a5b782'
address = '0x71d574755824C7A7100714791cb542C8157E8cF0'
nonce = w3.eth.getTransactionCount(address)
gasPrice = w3.eth.gasPrice
value = w3.toWei(0, 'ether')
signedTx = w3.eth.account.signTransaction(dict(
nonce = nonce,
gasPrice = gasPrice,
gas = 100000,
to = '0x0000000000000000000000000000000000000000',
value = value,
data= hashlib.sha256(json.dumps({
    'student': {
        'name': name,
        'surname': surname,
        'date_of_birth': birth_date.strftime('%Y-%m-%d'),
        'graduation_date': graduation_date.strftime('%Y-%m-%d'),
        'grade': grade,
        'degree': degree,
        'identifier': identifier
                    },
                }).encode('utf-8')).hexdigest()
            ), privateKey)

tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
txId = w3.toHex(tx)
print(txId)
print(value)