# Reference handling 

CountryA and CountryB are both authorized to use the gateway.
CountryC is unauthorized. 
The test cases cover the handling of references from their national backends


## upload reference

CountryA creates a reference and uploads it.
It must appear in the trustlist. 

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the response had no error
* check that the reference is in the trustlist 

## reference data distribution

CountryA creates a reference and CountryB can download it.
Another (simulated) gateway can also download the reference. 

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "OtherGateway" downloads the reference trustlist
* check that the reference is in the trustlist 
* "CountryB" downloads the reference trustlist
* check that the reference is in the trustlist

## delete reference

CountryA creates a reference and deletes it using
the defaulte endpoint

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the reference is in the trustlist 
* "CountryA" deletes uploaded reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the reference is NOT in the trustlist


## unauthorized delete reference

CountryB tries to delete a reference of CountryA.
The operation must not succeed. 

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the reference is in the trustlist 
* "CountryB" deletes uploaded reference
* check that the response had an error
* "CountryA" downloads the reference trustlist
* check that the reference is in the trustlist 

## unauthorized access to reference trustlist

* "CountryC" downloads the reference trustlist
* check that the response had an error

## unauthorized upload reference 1

CountryB attempts to upload a reference of CountryA

It must not appear in the trustlist. 
* "CountryA" creates a reference
* "CountryB" creates CMS message with trusted reference
* "CountryB" uploads CMS reference
* check that the response had an error
* "CountryA" downloads the reference trustlist
* check that the reference is NOT in the trustlist 

## unauthorized upload reference 2

CountryB attempts to upload a reference of CountryA
and has access  to CountryA's upload keys

It must not appear in the trustlist. 
* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryB" uploads CMS reference
* check that the response had an error
* "CountryA" downloads the reference trustlist
* check that the reference is NOT in the trustlist 


___

* delete uploaded reference
