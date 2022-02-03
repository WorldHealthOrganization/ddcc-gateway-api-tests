# Certificate handling 

CountryA is authorized to use the primary gateway. 
CountryC is authorized to use the secondary gateway. 
The test cases cover the handling of references from their national backends



## certificate federation

CountryA creates a certificate on the primary gateway and 
CountryC can download it from the secondary gateway


* "CountryA" creates a certificate
* "CountryA" creates CMS message with certificate
* "CountryA" uploads CMS certificate
* check that the response had no error
* "CountryA" downloads the certificate trustlist
* check that the certificate is in the trustlist 
* wait synchronization time
* "CountryC" downloads the federated certificate trustlist
* check that the certificate is in the trustlist 

___

* delete uploaded certificate
