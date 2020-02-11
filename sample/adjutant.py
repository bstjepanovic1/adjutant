from adjutant import config

config.template_path = "src/_template"

config.source_path = "src"

config.build_path = "build"

config.add_rule("src/*.h", r'\/\*\**\s+\@(?P<template>.*?)\s*(?P<data>\{.*?\})\s+\*\/')
