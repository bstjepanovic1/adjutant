BUILD_DIR=build/
HEADERS = $(shell find src -type f -name '*.h')
HEADER_DEPS = $(patsubst src/%.h, $(BUILD_DIR)/%.d, $(HEADERS))

all: $(HEADER_DEPS)

$(BUILD_DIR)/%.d: src/%.h
	adjutant $< -t src/_template
