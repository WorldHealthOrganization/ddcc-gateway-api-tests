# Reference handling 
CountryA is authorized to use the first gateway.
The test cases cover the handling of references from their national backends


## trusted reference federation
CountryA creates a reference on the primary gateway.

* "CountryA" creates a reference
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error
* "CountryA" downloads the reference trustlist
* check that the reference is in the trustlist

___

* delete uploaded reference
