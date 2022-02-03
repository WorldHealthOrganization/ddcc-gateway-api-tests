

from getgauge.python import step, data_store

from step_impl.util.certificates import create_certificate, create_cms_with_certificate

@step("<country> creates CMS message with trusted issuer")
def creates_cms_message_with_trusted_issuer_certificate(country):
    assert False, "Add implementation code"

@step("<country> creates CMS message with trusted reference")
def creates_cms_message_with_reference(country):
    assert False, "Add implementation code"

@step("<country> creates CMS message with certificate")
def creates_cms_message_with_certificate(country):
    data_store['scenario']['trusted.certificate.raw'] = create_certificate()