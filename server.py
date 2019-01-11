# Copyright 2019, SimSage Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import requests
import json

from flask import Flask
from flask import request
from flask_cors import CORS

# set these first!!!  see https://simsage.nz/api.html
securityId = "?"
organisationId = "?"
kbId = "?"

# double check values are set before execution
if securityId == "?":
    raise ValueError("you have not setup your keys, please visit https://simsage.nz/api.html first!")

# setup FLASK endpoint, allow CORS
app = Flask(__name__)
CORS(app, resources={r"/query/*": {"origins": "*"}})


# sanity check - check service is running from /
@app.route('/')
def index():
    return "SimSage Python Server"


# respond to a POST from our client
@app.route('/query', methods=['POST'])
def query():
    query_in = request.get_json()  # get the payload and read the required fields
    customerId = query_in["customerId"]
    query = query_in["query"]

    # setup the required SimSage headers
    headers = {"Content-Type": "application/json", "Security-Id": securityId, "API-Version": "1"}

    # setup data to be posted to SimSage
    data = {"query": query, "organisationId": organisationId, "kbId": kbId, "numResults": 10, "scoreThreshold": 0.5}

    # make the request to SimSage
    response = requests.post("https://cloud.simsage.nz/api/query/{}".format(customerId), data=json.dumps(data), headers=headers)

    # return the query result to our calling client - but not the other sensitive information
    response_data = response.json()
    if "error" in response_data:  # anything go wrong?
        raise ValueError(response_data["error"])
    return json.dumps(response_data["queryResultList"]), 200, {'ContentType': 'application/json'}


# non-gunicorn use - debug only
if __name__ == "__main__":
    logging.info("test only - using gunicorn to run properly, see README.md")
    app.run(host="0.0.0.0",
            port=9000,
            debug=True,
            use_reloader=False)
