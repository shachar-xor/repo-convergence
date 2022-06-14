enable_testing()

set(TARGET_NAME lib_test)

add_executable(${TARGET_NAME}
  weather_test.cc
)

target_include_directories(${TARGET_NAME} PRIVATE ${COMMON_LIB_DIR})

target_link_libraries(${TARGET_NAME}
  lib
  ${CONAN_LIBS_GTEST}
)

include(GoogleTest)
gtest_discover_tests(lib_test)
