from getgauge.python import step
from time import sleep

@step("wait for <15> seconds")
def wait_for_seconds(seconds):
    sleep(int(seconds))

@step("Reference <testcase>")
def reference(testcase):
    print(f'Reference to {testcase}')