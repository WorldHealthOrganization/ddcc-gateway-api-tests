# ---license-start
# eu-digital-green-certificates / dgc-api-tests
# ---
# Copyright [C] 2021 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 [the "License"];
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end

if False: 
    # Legacy code
    from os import environ, getcwd, path
    from os.path import join
    import json


    json_file_path = path.join('features', 'testing_environments.json')
    with open(json_file_path, 'r') as file:
        testenvs = json.load(file)
        testenv = testenvs['DEV']

    eu_gateway_url = testenv['eu_gateway_url']
    baseurl =  testenv['eu_gateway_url']

    first_gateway_url = testenv['first_gateway_url']

    verify = bool(testenv['verify'])

    certificateFolder = join(getcwd(), testenv["certificateFolder"])

    authCerts = (
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem"))

class FailedResponse:
    ok = False
    status_code = None
    text = None