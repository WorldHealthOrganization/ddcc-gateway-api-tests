# Certificate handling 

CountryA and CountryB are both authorized to use the gateway.
CountryC is unauthorized. 
The test cases cover the handling of certificates from their national backends


## upload certificate

CountryA creates a certificate and uploads it.
It must appear in the trustlist. 

* Reference "TXR-4999"
* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* Reference "TXR-4997"
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 

## certificate data distribution

CountryA creates a certificate and CountryB can download it.
Another (simulated) gateway can also download the certificate. 

* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* Reference "TXR-4994"
* Secondary gateway downloads the certificate trustlist
* check that the certificate is in the trustlist 
* Reference "TXR-4998"
* "CountryB" downloads the certificate trustlist
* check that the certificate is in the trustlist 

## delete certificate

CountryA creates a certificate and deletes it using
the defaulte endpoint

* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 
* "CountryA" deletes uploaded certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is NOT in the trustlist 

## delete certificate alternate endpoint

CountryA creates a certificate and deletes it using
the alternative endpoint (POST instead of DELETE)

* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 
* "CountryA" deletes uploaded certificate with alternate endpoint
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is NOT in the trustlist 


## unauthorized delete certificate

CountryB tries to delete a certificate of CountryA.
The operation must not succeed. 

* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 
* "CountryB" deletes uploaded certificate
* check that the response had an error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 

## unauthorized access to certificate trustlist

* "CountryC" downloads the certificate trustlist
* check that the response had an error

## unauthorized upload certificate 1

CountryB attempts to upload a certificate of CountryA

It must not appear in the trustlist. 
* "CountryA" creates a certificate
* "CountryB" creates CMS message with certificate
* "CountryB" uploads CMS certificate
* check that the response had an error
* "CountryA" downloads the certificate trustlist
* check that the certificate is NOT in the trustlist 

## unauthorized upload certificate 2

CountryB attempts to upload a certificate of CountryA
and has access  to CountryA's upload keys

It must not appear in the trustlist. 
* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryB" uploads CMS certificate
* check that the response had an error
* "CountryA" downloads the certificate trustlist
* check that the certificate is NOT in the trustlist 


___

* delete uploaded certificate
