# Trusted issuer handling 

CountryA and CountryB are both authorized to use the gateway.
CountryC is unauthorized. 
The test cases cover the handling of trusted issuer entries from their national backends
TODO: check the structure of the response?


## authorized access to trusted issuer trustlist

* "CountryA" downloads the trusted issuer trustlist
* check that the response had no error


## unauthorized access to trusted issuer trustlist

* "CountryC" downloads the trusted issuer trustlist
* check that the response had an error

