# ---license-start
# eu-digital-green-certificates / dgc-api-tests
# ---
# Copyright (C) 2021 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end

from os import environ, getcwd, path
from os.path import join

eu_gateway_url = environ.get('eu_gateway_url')
jrc_url = environ.get('jrc_url')

first_gateway_url = environ.get('first_gateway_url')
second_gateway_url = environ.get('second_gateway_url')
third_gateway_url = environ.get('third_gateway_url')

verify = bool(environ.get('third_gateway_url'))

certificateFolder = join(getcwd(), environ.get("certificatesFolder"))
authCerts = (
    path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem"))

class FailedResponse:
    ok = False
    status_code = None
    text = None