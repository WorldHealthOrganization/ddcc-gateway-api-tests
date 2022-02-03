# Meta data interface with 2 parties 

## Federated signatures can be download

* "CountryA" downloads federated signatures
* check that the response had no error

## Federated gateway appears in gateway list

* "CountryA" downloads the federated gateway list on "firstGateway" 
* check that the response had no error
* check that "secondGateway" is in the gateway list
* "CountryC" downloads the federated gateway list on "secondGateway"
* check that the response had no error
* check that "firstGateway" is in the gateway list


## Federated gateway appears in federator list

* "CountryA" downloads the federated federator list on "firstGateway" 
* check that the response had no error
* check that "secondGateway" is in the federator list
* "CountryC" downloads the federated federator list on "secondGateway"
* check that the response had no error
* check that "firstGateway" is in the federator list


## Federated endpoints are protected
* "CountryA" downloads the federated gateway list on "secondGateway" 
* check that the response had an error
* "CountryC" downloads the federated gateway list on "firstGateway" 
* check that the response had an error
* "CountryA" downloads the federated federator list on "secondGateway" 
* check that the response had an error
* "CountryC" downloads the federated federator list on "firstGateway" 
* check that the response had an error


## Meta data is accessible
* "CountryA" downloads the federation metadata on "firstGateway" 
* check that the response had no error
* check that meta data structure is OK
* "CountryC" downloads the federation metadata on "secondGateway"
* check that the response had no error
* check that meta data structure is OK


