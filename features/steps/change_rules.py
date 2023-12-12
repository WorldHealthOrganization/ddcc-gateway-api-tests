from behave import *
from datetime import datetime, timedelta


def change_rule(context, changeFunc):
    rule = context.rule
    changeFunc(rule)
    context.rule = rule


@step("change countrycode to a wrong format")
def change_countrycode_to_a_wrong_format(context):
    def change_countrycode(rule):
        rule["Country"] = rule["Country"] + "-"
    change_rule(change_countrycode)


@step("change countrycode to a wrong country")
def change_countrycode_to_a_wrong_country(context):
    def change_to_wrong_country(rule):
        if (rule["Country"] == "EN"):
            rule["Country"] = "DE"
        else:
            rule["Country"] = "EN"
    change_rule(change_to_wrong_country)


@step("change countrycode in Identifier to a wrong country")
def change_countrycode_in_identifier_to_a_wrong_country(context):
    def change_rule_identifier_to_wrong_country(rule):
        ruleId = rule["Identifier"]
        currentCountry = ruleId[3:5]
        if ( currentCountry == "EN"):
            newCountry = "DE"
        else:
            newCountry = "EN"
        rule["Identifier"] = ruleId[:3]+newCountry+ruleId[5:]
    change_rule(change_rule_identifier_to_wrong_country)


@step("change ValidFrom less than {hours}h")
def change_validfrom_less_than_h(context, hours: str):
    changeHours = int(hours)

    def change_valid_from(rule):
        # substract some time so that it definitly is less than
        rule["ValidFrom"] = datetime.now() + timedelta(hours=changeHours) - \
            timedelta(seconds=5)
    change_rule(change_valid_from)


@step("remove description of the Rule")
def remove_description_of_the_rule(context):
    def remove_description(rule):
        rule["Description"] = []
    change_rule(remove_description)


@step("change description to have less than {strLength} characters")
def change_description_to_have_less_than_characters(context, strLength):
    def change_description(rule):
        rule["Description"] = [
            {"lang": "en", "desc": "api-test-rule for use in api test"[:(int(strLength)-1)]}]
    change_rule(change_description)


@step("use only german in the description of the Rule")
def use_only_german_in_the_description_of_the_rule(context):
    def change_description(rule):
        rule["Description"] = [
            {"lang": "de", "desc": "api-test-rule for use in api test"}]
    change_rule(change_description)


@step("add language {language_code} in description")
def add_language_in_description(context, language_code: str):
    def change_description(rule):
        rule["Description"] = [{"lang": language_code, "desc": "api-test-rule for use in api test"}, {
            "lang": language_code, "desc": "api-test-rule for use in api test"}]
    change_rule(change_description)

@step("set version of the Rule to {version}")
def set_version_of_the_rule_to(context, version):
    def change_version(rule):
        rule["Version"] = version
    change_rule(change_version)

@step("set version of the schema to {version}")
def set_version_of_the_schema_to(context, version):
    def change_schema_version(rule):
        rule["SchemaVersion"] = version
    change_rule(change_schema_version)

@step("set ValidFrom more than {dayStr} days in the future")
def set_validfrom_more_than_days_in_the_future(context, dayStr):
    changeDays = int(dayStr)

    def change_valid_from(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(days=changeDays)
    change_rule(change_valid_from)

@step("set ValidFrom after ValidTo value")
def set_validfrom_after_validto_value(context):
    def change_valid_to_before_valid_from(rule):
        rule["ValidTo"] = rule["ValidFrom"] - timedelta(hours=2)
    change_rule(change_valid_to_before_valid_from)

@step("change ValidTo to {hoursStr}h before the current ValidTo")
def change_validto_to_1h_before_the_current_validto(context, hoursStr):
    hours = int(hoursStr)
    def change_valid_to(rule):
        rule["ValidTo"] = rule["ValidTo"] - timedelta(hours=hours)
    change_rule(change_valid_to)


@step("change ValidTo to {hoursStr}h after the current ValidFrom")
def change_validto_to_1h_before_the_current_validto(context, hoursStr):
    hours = int(hoursStr)
    def change_valid_to(rule):
        rule["ValidTo"] = rule["ValidFrom"] + timedelta(hours=hours)
    change_rule(change_valid_to)


def change_version_to(context, version):
    def change_version(rule):
        rule["Version"] = version
        context.new_version = version
    return change_version

@step("the {attributename} of the rule is changed to {attributevalue}")
def change_rule_to_new_version(context, attributename, attributevalue):
    ''' e.g. "When the Version of the rule is changed to 1.0.1" '''
    context.rule[attributename] = attributevalue
    #context.new_version = context.rule['Version']

@step("the rule becomes valid {seconds} seconds in the future")
def step_impl(context, seconds):
    context.rule['ValidFrom'] = datetime.now()+timedelta(seconds=int(seconds))


@step("change ValidFrom to {secStr}sec in the future")
def change_validfrom_to_sec_in_the_future(context, secStr):
    changeSeconds = int(secStr)

    def change_valid_from(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(seconds=changeSeconds)
    change_rule(change_valid_from)

@step("change ValidTo to {secStr}sec in the future")
def change_validto_to_sec_in_the_future(context, secStr):
    changeSeconds = int(secStr)

    def change_valid_to(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(seconds=changeSeconds)
    change_rule(change_valid_to)

@step("change CertificateType to be invalid")
def change_certificatetype_to_be_invalid(context):
    def change_valid_to(rule):
        (ruleType,country,counter) = rule["Identifier"].split("-")
        rule["CertificateType"] = "General" if ruleType=="VR" else "Vaccination"
    change_rule(change_valid_to)
