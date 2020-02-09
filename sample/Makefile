BUILD_DIR=build
HEADERS = $(shell find src -type f -name '*.h')
HEADER_DEPS = $(patsubst src/%.h, $(BUILD_DIR)/%.d, $(HEADERS))


# find all templates
TPL_DIR = src/_template
TPL_SRCS = $(shell find ${TPL_DIR} -type f -name '*.tpl')
# compile templates to python files
TPL_PYS = $(patsubst ${TPL_DIR}/%.tpl, $(BUILD_DIR)/__template__/%.tpl.py, $(TPL_SRCS))


all: $(HEADER_DEPS) $(TPL_PYS)

$(BUILD_DIR)/%.d: src/%.h
	adjutant process $< -t src/_template -t $@


# compile templates to python files
$(BUILD_DIR)/__template__/%.tpl.py: ${TPL_DIR}/%.tpl
	adjutant template:compile $< -o $@
