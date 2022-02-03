# Trusted issuer handling 

CountryA is authorized to use the first gateway. 
CountryC is authorized to use the second gateway. 
The test cases cover the handling of issuer entries from their national backends



## trusted issuer federation

CountryA creates a trusted issuer on the primary gateway and 
CountryC can download it from the secondary gateway

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 
* wait synchronization time
* "CountryC" downloads the federated issuer trustlist
* check that the trusted issuer is in the trustlist 

___

* delete uploaded trusted issuer entry

