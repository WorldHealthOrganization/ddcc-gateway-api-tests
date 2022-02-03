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
- Install the required libraries with `pipenv install` or install them manually 

## Preparations

The `certificates` folder holds the client certificates of the simulated national backends.
<pre>
Folder structure: 
 [certificates] 
  + (client certs for EU test cases)
  +--[secondCountry]
  |   + (client certs for EU test cases)
  +--[CountryA]
  |   + (client certs for WHO DDCCG test cases)
</pre>

## Licensing

Copyright (C) 2021 T-Systems International GmbH and all other contributors

Licensed under the **Apache License, Version 2.0** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License.
