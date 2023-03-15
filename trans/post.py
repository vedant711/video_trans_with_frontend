import requests


# client = requests.session()
# print(client)
url= 'http://192.168.1.203:8305/api'
# client.get(url,verify=False)
# csrftoken = client.cookies['csrf']
# client.get(url)  # sets cookie
# print(client.cookies)
# if 'csrftoken' in client.cookies:
#     csrftoken = client.cookies['csrftoken']
# else:
#     csrftoken = client.cookies['csrf']

# print(data)
header = {"Authorization":'60ea74a6edd466cf71852da61e618f470ed35208'}
data = {'url':'https://drive.google.com/uc?id=1Oi06ryqoqWHdQo_RUE5YlIDTETeRssZ-','callback':'http://192.168.1.203:8304/check'}
x=requests.post(url,data=data,headers=header)

print(x)
