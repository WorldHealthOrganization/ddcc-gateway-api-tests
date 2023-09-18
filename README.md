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

## Test data (onboarded virtual countries)

The folder `certificates` should host the key material of the
fictional countries that are used for testing. 

The directory structure is as follows: 
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

## Usage

A testing environment must be specified with each execution:

```
behave -D testenv=UAT 
```

## Licensing

Copyright (C) 2022 T-Systems International GmbH and all other contributors

Licensed under the **Apache License, Version 2.0** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License.
