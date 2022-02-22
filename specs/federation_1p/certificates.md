# Certificate handling
CountryA is authorized to use the first gateway.
The test cases cover the handling of certificates from their national backends


## certificate federation
CountryA creates a certificate on the primary gateway

* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS with certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the response had no error
* check that the certificate is in the trustlist

___

* delete uploaded certificate

