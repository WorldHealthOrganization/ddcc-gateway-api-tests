# Trusted issuer handling 

CountryA is authorized to use the first gateway. 
CountryC is authorized to use the second gateway. 


## authorized access to trusted issuer trustlist GW1
Foreign issuers do not appear in the default trust list, only if federated=true

* "CountryA" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one issuer with "country" = "XA" is in the trustlist
* check that no issuer with "country" = "XC" is in the trustlist


## authorized access to trusted issuer trustlist GW2
Foreign issuers do not appear in the default trust list, only if federated=true

* select gateway "2"
* "CountryC" downloads the trusted issuer trustlist
* check that the response had no error
* check that at least one issuer with "country" = "XC" is in the trustlist
* check that no issuer with "country" = "XA" is in the trustlist


## unauthorized access to trusted issuer trustlist GW1 

* "CountryC" downloads the trusted issuer trustlist
* check that the response had an error

## unauthorized access to trusted issuer trustlist GW2

* select gateway "2"
* "CountryA" downloads the trusted issuer trustlist
* check that the response had an error


## federated issuers can be read GW1

* skip until two-way sync is turned on
* "CountryA" downloads the federated issuer trustlist
* check that the response had no error
* check that at least one issuer with "country" = "XC" is in the trustlist


## federated issuers can be read GW2

* select gateway "2"
* "CountryC" downloads the federated issuer trustlist
* check that the response had no error
* check that at least one issuer with "country" = "XA" is in the trustlist
* check that at least one issuer with "country" = "XB" is in the trustlist
