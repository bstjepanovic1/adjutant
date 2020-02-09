from adjutant.config import add_rule

TEMPLATE_PATH = "src/_template"

SOURCE_PATH = "src"

BUILD_PATH = "build"

add_rule("src/*.h", r'\/\*\**\s+\@(?P<func>.*?)(?P<data>\{.*?\})\s+\*\/')
