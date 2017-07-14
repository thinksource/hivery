# REAMDME

The project base on Flask and python3.6

## Install

> pip install -r requirements.txt

## How to run

>python main.py

## API intereface

- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.

service address: http://127.0.0.1:5000/company/companyname

- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.

service address: http://127.0.0.1:5000/common

sample post json is samplerequest2.json

- Same as feature2 but only  send just the user id. and return the user names

service address: http://127.0.0.1:5000/commonid/id1/id2

only array of user name as result

- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface: { "username": "Ahi", "age":"30", "fruits":["banana", "apple"], "vegetables":["beetroot", "lettuce"]}

service address: http://127.0.0.1:5000/user/username

notice: the use name must use html encode, for example Decker Mckenzie should be Decker%20Mckenzie
