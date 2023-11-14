msg = ""

while True:
    a = input()
    if a != '':
        msg += "'" + a + "',\n"
    else:
        break

print(msg)