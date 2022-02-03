# Reference handling 

CountryA is authorized to use the first gateway. 
CountryC is authorized to use the second gateway. 
The test cases cover the handling of references from their national backends



## trusted reference federation

CountryA creates a reference on the primary gateway and 
CountryC can download it from the secondary gateway

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the reference is in the trustlist 
* wait synchronization time
* "CountryC" downloads the federated reference trustlist
* check that the reference is in the trustlist 

___

* delete uploaded reference
