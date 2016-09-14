from behave import *
import os
import subprocess

@given('we have the example presentation')
def step_impl(context):
    if os.path.exists("example/example.html"):
        context.filename = "example/example.html"
        return
    assert False

@given('the output directory is empty')
def step_impl(context):
    if os.path.isdir("output"):
        subprocess.call(["rm","-r","output/*"])

@when ('we run convert on it')
def step_impl(context):
    print("Running convert on %s"%context.filename)
    res = subprocess.call(["./convert.py", context.filename])
    assert res == 0

@then ('the output directory contains the first slide')
def step_impl(context):
    assert os.path.exists("output/slide1.html")
