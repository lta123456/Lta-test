import requests


s = requests.session()
HOST = r'http://121.41.14.39:8082/user/list'#'http://ip:port'
NAME_PSW = {'username':'ka0518','password':'C607D58E3618832F937D80D500A6046C'}
print(s.get(HOST).json())