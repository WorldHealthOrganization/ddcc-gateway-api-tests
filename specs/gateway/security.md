# Basic security test cases

CountryA and CountryB are both authorized to use the gateway.
CountryC is unauthorized.

## Fake authentication headers 

CountryC has been able to get the public parts of CountryA's 
AUTH certificate and is trying to fake the headers that the 
ingress is setting. 

* extract subject and fingerprint from "auth" certificate of "CountryA" 
* "CountryC" uses its "auth" cert with fake headers for access
* check that the response had an error
