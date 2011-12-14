
import sys
from drest.connection import Connection

conn = Connection('http://localhost:8000/api/v0',
                  serialize=True)
conn.auth(dmirr_api_user='derks', 
          dmirr_api_key='a851d9f6485bf27c3336775190e9da97d14c8083')
#res, data = conn.request('GET', '/user/2')
conn.add_resource('user')
res,data = conn.user.get()

for user in data['objects']:
    print "%s -> %s" % (user['username'], user['first_name'])


response, data = conn.user.get(2)

new_data = data.copy()
new_data['first_name'] = 'John'
new_data['last_name'] = 'Doe'

response, data = conn.user.update(2, new_data)
print response.unserialized_content
#conn.user.get(1)
