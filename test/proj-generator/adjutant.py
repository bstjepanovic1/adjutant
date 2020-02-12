import json
from adjutant import config

config.template_path = 'src/_template/'

config.source_path = 'src/'

config.build_path = 'build/'

def run_template(processor, match):
    processor.template(match.group('template'), json.loads(match.group('data')))

config.add_rule(
    "src/*.h", 
    r'\/\*\**\s+\@(?P<template>.*?)\s*(?P<data>\{.*?\})\s+\*\/', run_template)
