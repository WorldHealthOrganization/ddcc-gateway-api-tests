# Certificate handling 

CountryA is authorized to use the first gateway. 
CountryC is authorized to use the second gateway. 
The test cases cover the handling of certificates from their national backends


## certificate federation

CountryA creates a certificate on the primary gateway and 
CountryC can download it from the secondary gateway

* skip (remove this line to actually execute)
* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS with certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 
* wait for "300" seconds
* set filter for "withFederation" to "true"
* "CountryC" downloads the certificate trustlist
* check that the certificate is in the trustlist 

## trusted certificate federation based on existing data

* select gateway "2"
* "CountryC" downloads the certificate trustlist
* check that the response had no error
* check that no entry with "country" = "XA" is in the response
* check that no entry with "country" = "XB" is in the response
* check that at least one entry with "country" = "XC" is in the response
* set filter for "withFederation" to "true"
* "CountryC" downloads the certificate trustlist
* check that the response had no error
* check that at least one entry with "country" = "XA" is in the response
* check that at least one entry with "country" = "XB" is in the response
* check that at least one entry with "country" = "XC" is in the response



___

* delete uploaded certificate
