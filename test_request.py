import http.client
 
conn = http.client.HTTPSConnection("api.uc.cl")
 
payload = ""
 
headers = {

    'User-Agent': "insomnia/2023.5.8",

    'X-Api-Key': "Rs05SNcp1SOBXYkw3KTyxUBP6b1iinWAq7IbiAE6  "

    }
print("Enviando request...") 
conn.request("GET", "/tarjetauc/v1/user/A31802C7?buscar=mifare", payload, headers)
print("Request enviada...") 
res = conn.getresponse()

data = res.read()
 
print(data.decode("utf-8"))
