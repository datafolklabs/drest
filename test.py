
from drest.connection import Connection

conn = Connection('http://localhost:8000/api/v0',
                  deserialize=True)
conn.auth(dmirr_api_user='derks', 
          dmirr_api_key='837e2a86a66accf213cf1ddbe49d6c44f993c934')
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
