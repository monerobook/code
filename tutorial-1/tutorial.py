# Mastering Monero Tutorial. This is a comment

import requests
import json

# Import Setup variables
# Url for JSON RPC interface. We assume that your RPC interface is running on localhost port 18082

url = "http://localhost:18082/json_rpc"

# JSON headers . Required.

headers = {"content-type”: “application/json”}

# RPC input . Adding method name , at the moment we do not need variables.

rpc_fields = {
"method" : "get_balance"
}

# Adding the JSON RPC version and id. Id is a int variable which should be incrementated each request. First request is 0 , second is one ...

rpc_fields.update({"jsonrpc": "2.0", "id”: "0"})

# Execute the rpc request

response = requests.post(url,data=json.dumps(rpc_fields),headers=headers)

# Print the response as JSON

print(json.dumps(response.json()))
