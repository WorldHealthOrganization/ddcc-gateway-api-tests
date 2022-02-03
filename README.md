<h1 align="center">
   DDCC Gateway  API Tests
</h1>

## General info and requirements

The test suite is based on Gauge with a Python backend. The test cases are written in human readable language in the form of markdown
files. Each headline marks a test case and each list element marks a test case step. Every test case step is linked to a function in
python code which contains the definition of the test step. 

Requirements: 
- Gauge (https://gauge.org/) 1.3 or later
- Python (https://gauge.org/) 3.9 or later

Installation instructions: 

- Install gauge and python
- Clone the repository
- In the repository:
```
pipenv install
pipenv shell
```

## Preparations

The `certificates` folder holds the client certificates of the simulated national backends.
<pre>
Folder structure: 
 [certificates] 
  + (client certs for EU test cases)
  +--[secondCountry]
  |   + (client certs for EU test cases, second country)
  +--[CountryA]
  |   + (client certs for WHO DDCCG test cases)
  +--[CountryB]
  |   + (client certs for WHO DDCCG test cases)
  +--[CountryC]
  |   + (client certs for WHO DDCCG test cases)
</pre>

In each folder (=for each test country), the following files are expected: 
| file name                    | description                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| auth.pem                     | PEM encoded Authentication (NBTLS) certificate                                          |
| key_auth.pem                 | PEM encoded private key of the Authentication (NBTLS) certificate                       |
| csca.pem                     | PEM encoded CSCA (NBCSCA) certificate                                                   |
| key_csca.pem                 | PEM encoded private key of CSCA (NBCSCA) certificate                                    |
| upload.pem                   | PEM encoded Upload (NBUS) certificate                                                   |
| key_upload.pem               | PEM encoded private key of Upload (NBUS) certificate                                    |


## Configuration

In order to run the tests multiple certificates are needed to create DSC certificates and to authenticate against the DGC-Gateway.

Gauge supports multiple environments in which the configuration can change. For that reason a `.gitignore` file is configured in order to use a local environment. In order to change the eu_gateway_url a config file at `/env/local/defaupt.properties` is needed. This file can look like this:

```properties
eu_gateway_url = https://gateway.url
first_gateway_url = http://address.of.test.first.gateway
second_gateway_url = http://address.of.test.second.gateway
third_gateway_url = http://address.of.test.third.gateway

# http_proxy = http://only.if.required
# https_proxy = http://only.if.required
```

Also some Authentication/UPLOAD/CSCA certificates are needed in order to upload and delete certificates. The folder structure looks like this:

| file name                    | description                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| auth.pem                     | PEM encoded Authentication (NBTLS) certificate                                          |
| key_auth.pem                 | PEM encoded private key of the Authentication (NBTLS) certificate                       |
| csca.pem                     | PEM encoded CSCA (NBCSCA) certificate                                                   |
| key_csca.pem                 | PEM encoded private key of CSCA (NBCSCA) certificate                                    |
| upload.pem                   | PEM encoded Upload (NBUS) certificate                                                   |
| key_upload.pem               | PEM encoded private key of Upload (NBUS) certificate                                    |


## Execution

Gauge is used for the execution of the test cases. For this ```gauge run --env local specs/spec_file_or_folder``` is used to run the test cases against the local configuration. For more information on how the execution can be tweaked are in the [gauge documentation](https://docs.gauge.org/execution.htmlos=windows&language=python&ide=vscode#multiple-arguments-passed-to-gauge-run).


## Licensing

Copyright (C) 2022 T-Systems International GmbH and all other contributors

Licensed under the **Apache License, Version 2.0** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License.
