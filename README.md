<h1 align="center">
   DDVC Gateway  API Tests
</h1>

## General info and requirements

The test suite is based on the *Behave* framework, a Python implementation of *Cucumber*. 
Tests are written in *Gherkin*, a human-readable, behavior focussed syntax.

Requirements: 
- Python (https://gauge.org/) 3.9 or later

Installation instructions: 

- Install Python
- Clone the repository
- In the repository:
```
# Optional: Create venv
# python -m venv .venv --prompt DDVC
# source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Usage

A testing environment must be specified with each execution:

```
behave -D testenv=UAT 
```

The test cases will then look into the corresponding folders for testing certificates.
For the countries which are set as country A and country B, these certificates must 
be onboarded on the respective testing environment.

### Testing environments 

A testing environment definition currently consists of 
 - an endpoint
 - three roles, representing a country's software client. 
      - The countries are aliased A, B and C.
      - A and B are onboarded countries
      - C is not onboarded and used for negative tests

The environments are defined in the file `features/testing_environments.json`. 

Example: 
```
    "UAT": {
        "base_url" : "https://tng-uat.who.int",
        "country_A" : "XXA",
        "country_B" : "XXB",
        "country_C" : "XXC"
    },
    "Scandinavia": {
        "base_url" : "https://virtual.scandinavia.test",
        "country_A" : "FIN",
        "country_B" : "SWE",
        "country_C" : "NOR"
    }
```
### Virtual countries 

Some environments do not want to use real country codes. 
In order for them to function, non-existent (virtual) countries 
must be defined in `features/testing_countries.json`.

There, they must be assigned a unique 2-letter and 3-letter country
code which must not already be used by an existing country.


### Test data (onboarded virtual countries)

The folder `certificates` should host the key material of the
fictional countries that are used for testing. 

The directory structure is as follows: 
 - top level: 3-letter country code
 - 2nd level: domain

Example: 
```
certificates
    +--- XXA                 (country XA)
    |     +--- DDC           (domain DCC)
    |     |     +--- TLS.pem
    |     |     +--- TLS.key
    |     |     +--- SCA.pem
    |     |     +--- SCA.key
    |     |     +--- UP.pem
    |     |     +--- UP.key
    |     +--- DIVOC         (possible other domain)
    |           +--- TLS.pem
    |           +--- ...
    |
    +--- XXB                 (country XB)
          +--- DCC
                +--- TLS.pem
                +--- ...
```

## Licensing

Copyright (C) 2022 T-Systems International GmbH and all other contributors

Licensed under the **Apache License, Version 2.0** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License.
