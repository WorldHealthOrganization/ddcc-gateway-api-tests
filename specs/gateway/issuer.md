# Trusted issuer handling 

CountryA and CountryB are both authorized to use the gateway.
CountryC is unauthorized. 
The test cases cover the handling of trusted issuer certificates from their national backends


## upload trusted issuer

CountryA creates a trusted issuer entry and uploads it.
It must appear in the trustlist. 

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 

## trusted issuer certificate data distribution

CountryA creates a trusted issuer entry and CountryB can download it.
Another (simulated) gateway can also download the trusted issuer certificate. 

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* Secondary gateway downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 
* "CountryB" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 

## delete trusted issuer certificate

CountryA creates a trusted issuer entry and deletes it using
the defaulte endpoint

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 
* "CountryA" deletes uploaded trusted issuer certificate
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is NOT in the trustlist 

## delete trusted issuer certificate alternate endpoint

CountryA creates a trusted issuer entry and deletes it using
the alternative endpoint (POST instead of DELETE)

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 
* "CountryA" deletes uploaded trusted issuer certificate with alternate endpoint
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is NOT in the trustlist 


## unauthorized delete trusted issuer certificate

CountryB tries to delete a trusted issuer certificate of CountryA.
The operation must not succeed. 

* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryA" uploads CMS with trusted issuer
* check that the response had no error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 
* "CountryB" deletes uploaded trusted issuer certificate
* check that the response had an error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is in the trustlist 

## unauthorized access to trusted issuer trustlist

* "CountryC" downloads the trusted issuer trustlist
* check that the response had an error

## unauthorized upload trusted issuer 1

CountryB attempts to upload a trusted issuer certificate of CountryA

It must not appear in the trustlist. 
* "CountryA" creates a trusted issuer entry
* "CountryB" creates CMS message with trusted issuer
* "CountryB" uploads CMS with trusted issuer
* check that the response had an error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is NOT in the trustlist 

## unauthorized upload trusted issuer 2

CountryB attempts to upload a trusted issuer certificate of CountryA
and has access  to CountryA's upload keys

It must not appear in the trustlist. 
* "CountryA" creates a trusted issuer entry
* "CountryA" creates CMS message with trusted issuer
* "CountryB" uploads CMS with trusted issuer
* check that the response had an error
* "CountryA" downloads the trusted issuer trustlist
* check that the trusted issuer is NOT in the trustlist 


___

* delete uploaded trusted issuer entry
