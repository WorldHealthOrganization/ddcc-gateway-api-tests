# Create Testdata that stays on the environment

## Certificate CountryA

CountryA creates a certificate and uploads it.

* "CountryA" creates a certificate with expiry "365" days
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS with certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 


## Certificate CountryB

CountryB creates a certificate and uploads it.

* "CountryB" creates a certificate with expiry "365" days
* "CountryB" creates CMS message with certificate
* "CountryB" uploads CMS with certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 

## Certificate CountryC

CountryC creates a certificate and uploads it.

* select gateway "second_gateway"
* "CountryC" creates a certificate with expiry "365" days
* "CountryC" creates CMS message with certificate
* "CountryC" uploads CMS with certificate
* check that the response had no error
* "CountryC" downloads the certificate trustlist
* check that the certificate is in the trustlist 





