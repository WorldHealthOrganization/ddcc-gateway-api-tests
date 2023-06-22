# Create Testdata that stays on the environment

## Reference Data A

* "CountryA" creates a reference
* modify reference set "name" to "Permit A38"
* modify reference set "domain" to "SHC"
* modify reference set "url" to "https://this.does.not/exist/just/testing"
* "CountryA" creates CMS message with trusted reference
* "CountryA" uploads CMS reference
* check that the response had no error


## Reference Data B

* "CountryB" creates a reference
* modify reference set "name" to "Circular B65"
* modify reference set "domain" to "ICAO"
* modify reference set "url" to "https://this.does.not/exist/just/testing"
* "CountryB" creates CMS message with trusted reference
* "CountryB" uploads CMS reference
* check that the response had no error


## Reference Data C

* select gateway "second_gateway"
* "CountryC" creates a reference
* modify reference set "name" to "Permit A38"
* modify reference set "domain" to "DIVOC"
* modify reference set "url" to "https://this.does.not/exist/just/testing"
* "CountryC" creates CMS message with trusted reference
* "CountryC" uploads CMS reference
* check that the response had no error




