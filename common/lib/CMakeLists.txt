
set(TARGET_NAME lib)

add_library(${TARGET_NAME} STATIC
    weather.c
    weather.h
)

target_link_libraries(${TARGET_NAME} ${CONAN_LIBS})

add_subdirectory(ut)
enable_testing()
include(GoogleTest)
