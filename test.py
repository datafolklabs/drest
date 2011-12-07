
from drest.connection import Connection

conn = Connection('http://localhost:8000/api/v0')
conn.auth(dmirr_api_user='derks', 
          dmirr_api_key='837e2a86a66accf213cf1ddbe49d6c44f993c934')
res, data = conn.request('GET', '/user/2')
print data
#conn.user.get(1)
