# Migration plan for test suite

## Motivation

The test suite for the EU DCC gateway was implemented using the Gauge framework. 
Within the new project environment this would be an isolated solution as tests
are automated with Gherkin/Cucumber there. 

Further, some features from the EU gateway have been discontinued and other 
features have been added.

We have decided to migrate the test suite to Behave therefore, which is the 
Python implementation of Gherkin/Cucumber. 

## Spec Files

| Spec File |  Migration Decision |  
|---|---|
| `gateway/issuer.md` | Migrated to `issuer.feature` | 
| `gateway/security.md`  | Migrated to `security.feature` |
| `gateway/reference.md`| |
| `gateway/certificates.md`| |
| `eugateway/rules/UpdateRules.md`| Migrated to `update_rules.feature` |
| `eugateway/rules/GetRules.md` | Migrated to `get_rules.feature` |
| `eugateway/rules/UploadRules.md`| Migrated to `upload_rules.feature` |
| `eugateway/rules/DeleteRule.md`| |
| `eugateway/valuesets/GetValueset.md`| Migrated to `valuesets.feature` |
| `eugateway/rules_content_checks/ContentChecks.md`|   | 
| `eugateway/rules_content_checks/ContentChecksInvalidationRules.md`|   |
| `eugateway/rules_content_checks/ContentChecksAcceptanceRules.md`|   | 
| `eugateway/cms_migration/cmsmigration.md` | ❌ discontinued | 
| `eugateway/dcc/DeltaDownload.md`|❌ discontinued | 
| `eugateway/dcc/TrustList.md` | Migrated to `trustlist.feature` |
| `eugateway/dcc/CertificateHandling.md` | Migrated to `dsc.feature` | 
| `eugateway/revocation/UpDownDelete.md` | ❌ discontinued (Revocation Feature) | 
| `federation_2p/issuer.md` <br> `federation_2p/reference.md`  <br> `federation_2p/certificates.md` | ❌ discontinued (Federation) |