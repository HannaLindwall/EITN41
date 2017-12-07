import requests
import binascii
import numbers
requests.packages.urllib3.disable_warnings()

def submit(name, grade, signature):
    payload = {'name': name, 'grade': grade, 'signature': signature}
    request = (requests.get('https://eitn41.eit.lth.se:3119/ha4/addgrade.php',
                            params=payload, verify=False))
    return request.elapsed.total_seconds(), request.text

def hexHash(concat):
    return hashlib.sha1(concat.encode()).hexdigest()

def fakesig(name, grade, signature, hexchars):
    while len(signature) <= 20:
        times = []
        for x in range(0, len(hexchars)):
            time, result = submit(name, grade, (signature + hexchars[x]))
            if  result.strip() == "1":
                signature += hexchars[x]
                return signature, result
            times.append(time)
        signature += hexchars[times.index(max(times))]
        print(signature)
    return signature, result

signature = ""
name = "Kalle"
grade = 5
hexchars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
final_signature, result = fakesig(name, grade, signature, hexchars)
print(final_signature)
print(result)
