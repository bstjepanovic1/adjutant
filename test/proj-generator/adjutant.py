import json
from adjutant import config

config.template_path = 'src/_template/'

config.source_path = 'src/'

config.build_path = 'build/'

def run_template(processor, match):
    processor.template(match.group('template'), json.loads(match.group('data')))

config.add_rule(
    "src/*.h", 
    run_template, 
    r'\/\*\**\s+\@(?P<template>.*?)\s*(?P<data>\{.*?\})\s+\*\/'
)

def command_rule(processor):
    print("Found command rule", processor.source)

config.add_rule("src/*.b", command_rule)
