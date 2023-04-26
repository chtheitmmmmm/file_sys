import  sys
from urllib.parse import quote
from urllib.request import Request
import ssl

host = 'https://eid.shumaidata.com'
path = '/eid/check'
method = 'POST'
appcode = 'cf531c4214de4801ba1a3efe0e1d7435'
querys = f'idcard=421182200304260430&name={quote("程闽")}'
bodys = {}
url = host + path + '?' + querys

request = Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib2.urlopen(request, context=ctx)
content = response.read()
if (content):
    print(content)