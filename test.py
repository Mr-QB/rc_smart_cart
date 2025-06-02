import requests

url = "http://222.255.214.82:18888/users/add"  # URL API của bạn

# Cookie từ phiên đăng nhập (copy nguyên cookie bạn có)
cookies_str = "REC_T_ID=9ab93ac8-0564-11f0-918c-6edc3d7300ee; SPC_F=56H1XrNmyycU2eNn5Xo3jDXIfiqX7TDW; LIVE_STREAMING_UUID_KEY=YtAtb7reOs2pT2tvl28Ao1drPoBivJdg; SC_DFP=pdgfCxeZNbnngEiAkvbLzmqmxfcqgOTV; SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; SC_SSO=-; SC_SSO_U=-; _hjSessionUser_868286=eyJpZCI6ImJhM2NkYzhjLTI5M2EtNTc3Zi1hOGM1LWE0MDg1YzY3M2I0MCIsImNyZWF0ZWQiOjE3NDI0NTkwMzMzNzYsImV4aXN0aW5nIjp0cnVlfQ==; SPC_U=-; SPC_SI=m5UuaAAAAABITWw3Q0x4NH2zGAEAAAAAYVd0TFFWQVQ=; SPC_SEC_SI=v1-ZUpRUWdGckRYS3lqOWppeUQpGbLPv88MZHyIRUxwoHuUj/NXeIuxes8dBuZ7xL33c/8g/7LxoCsNSL3ZfTg2CzcK9ScD/qYd3na/zczN8XE=; SPC_R_T_ID=adT92ovLt6RG5kAUi/9jQA45g8DmLyzihvbtagOLPP+Wc0TkNZrvGFDICEwaQ9gGV7rbLBMysAyJA9Xq1QwV0x7gHZgi8j54hMQMHgBUfvoQdUFi5Yhq5wo+CQ9Gr+fE+v9aa7QXQPM0FtBENf82cZIzKLjH8iurqEQ9b29vKZ4=; SPC_R_T_IV=QTYycFNtYmVwc0V3ckRBTg==; SPC_T_ID=adT92ovLt6RG5kAUi/9jQA45g8DmLyzihvbtagOLPP+Wc0TkNZrvGFDICEwaQ9gGV7rbLBMysAyJA9Xq1QwV0x7gHZgi8j54hMQMHgBUfvoQdUFi5Yhq5wo+CQ9Gr+fE+v9aa7QXQPM0FtBENf82cZIzKLjH8iurqEQ9b29vKZ4=; SPC_T_IV=QTYycFNtYmVwc0V3ckRBTg==; SPC_SEC_SI=v1-VjJHcFVHYVJqZExVeFJpbjnX/VBVCUWza5/du5q46D/dfe+uOU6h6zDKzvwdADjgR0nrD/LC78FZF5TbWrbdb6G+SWmA20fXIYGrJyK+YUs=; SPC_SI=m5UuaAAAAABITWw3Q0x4NH2zGAEAAAAAYVd0TFFWQVQ=; SPC_SEC_SI=v1-VTFneDFvQ2QwNFh3WnZBM0Gntwn10snfzXItkjGcdThg30lZlkEhFY2hY040vcVyqWbhVvUe/HvxSpP/cWLR4f1DlqVVxgNjGmg4CM074UU=; SPC_ST=.aHFIYVpVMkdvdXRJSHdRdQTjb7jHWLbWTaR6qS9nRAVvdoi+U97EF91st0AW2bk70qYa7Xeh5VE79HLPJ5SN+sFDk84MXFMRzt/eR3CcFdM9GNrfyGcpsvTjwh1belHHNPdAjeha+HFbQSCQm5gJ096Kn7+IzTTgBG/+nCA5bUnTFB9i0vUHZ9pAI6xSlrlAVm9UQF0QS5ylT7TOk4uPXxCN0Yv0K4xTvBk1CNLZXdjxqdmkIw4/Zf2HXv6YeuVJ; SPC_EC=.SEY5Qk1iOHJaWldGUmphVw0ifYMm2AvKQwKrV+ajpVYg+IjMLr/aL97XV947GyDAz0xrqNwBjbUhgm6faEaQzuss8WeQz6gwtwhcPTeq+cKtGx3AZ9X8B57Ty29lJv4sJqZMjV7BVJGX0J74BoyiR2NJmSE0w2qQKWENpP9sUpu//8FjDzAm8LpXBS49JnmRrgIgz38gBKH6bhecS35nqiy+354b4BYkOQtQGBQ4AooInrlh6h6KFWQKclxKZpsB; SPC_SC_SESSION=g/nB2jKvHZidDzz7s2v67BC3RiHyZ01o+fXY4yPP1umR51DYUO1dQlfIFcu7qn0xeQiR0LtWxotBO5L7m3KDJkhY8cAY6onmK0yJgovaB44H50cHbgP0sgyG24OgkM3/eqTqmf9JIK3pirr0IODrF/oIJcTB13AoKHGujXG0/fCAbj5kZjbvmkIcfES7a88967cqs5liE8XO7e797d5F4B1+VOeKfqA7ne/Vm8yQXOHi0AoXgf6uZZu0H36uaN9l+JkIeIJvplW+Nsojx2rhZug==_1_1343711571; SPC_STK=RhwRNiAMxiGSDGFtz0oYGx0CanJrD4AThfktXxMY+vYSlE+QG0IU3hX1F2iIXtlhZGOCrJiyMZMHa6MpxDV+fPnvq/fesC4I7wZX/SftUcdJadXTKsnBqI3DQChOlZ2+V4dgT2aKPUTRvo01/VsM4AKkDF4IYXSPFE+yAlrc7hA9C5jEBxJMlkF6zeO774BRHSWNl6c0U9nYAcL1eCmVJGUMIyVxFYQFH3DxyFnzNjlQlIRF3OUnERmjVHYYhS28zfF3AX19uA5HJsg8e4VBcHmnwzt2bYjl/nB/WRK5nYDXyx3gDaZ/sESfUvXhwMmpqVYM4zp4tYb6IDMedaZZG7VeHTj3DCHcVegbZNdbZFDL+hyYr1Hj6n78zdxWlcKs8LBYZ3leTAlX5IaIzN3FINVljMjUD2+6K/SrwJcAy/8bTzETJNfipPzb1j1re2ptxscej9G5ArdtZEQj+30cNE4SqKRr1APDJp32tcqkhALMScVDczR6yTqhTfRNLmdH; CTOKEN=%2FrVPIT9qEfCphT6sqBOrhw%3D%3D"
# Chuyển cookie string thành dict
cookies = {}
for cookie in cookies_str.split(";"):
    if "=" in cookie:
        key, value = cookie.strip().split("=", 1)
        cookies[key] = value
print("Cookies:", cookies)
# Dữ liệu POST
data = {
    "username": "newuser",
    "password": "123456",
    "type": "1",
    "balance": "1000",
    "ref": "some_ref",
}

# Gửi POST request với data và cookie
response = requests.post(url, data=data, cookies=cookies)

print("Status code:", response.status_code)
print("Response text:", response.text)
