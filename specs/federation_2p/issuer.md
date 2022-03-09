# Trusted issuer handling 

CountryA is authorized to use the first gateway. 
CountryC is authorized to use the second gateway. 


## authorized access to trusted issuer trustlist GW1
Foreign issuers do not appear in the default trust list, only if federated=true

* "CountryA" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one entry with "country" = "XA" is in the response
* check that no entry with "country" = "XC" is in the response


## authorized access to trusted issuer trustlist GW2
Foreign issuers do not appear in the default trust list, only if federated=true

* select gateway "2"
* "CountryC" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one entry with "country" = "XC" is in the response
* check that no entry with "country" = "XA" is in the response


## unauthorized access to trusted issuer trustlist GW1 

* "CountryC" downloads the trusted issuer trustlist
* check that the response had an error

## unauthorized access to trusted issuer trustlist GW2

* select gateway "2"
* "CountryA" downloads the trusted issuer trustlist
* check that the response had an error


## federated issuers can be read GW1

* skip until two-way sync is turned on
* set filter for "withFederation" to "true"
* "CountryA" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one entry with "country" = "XC" is in the response


## federated issuers can be read GW2

* select gateway "2"
* set filter for "withFederation" to "true"
* "CountryC" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one entry with "country" = "XA" is in the response
* check that at least one entry with "country" = "XB" is in the response
