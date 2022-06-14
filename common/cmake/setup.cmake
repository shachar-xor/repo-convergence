
include(${CMAKE_SCRIPT_DIR}/definitions.cmake)

enable_testing()

if (IS_WINDOWS)
    include(CSharpUtilities)
endif()

include(${CMAKE_SCRIPT_DIR}/folders.cmake)
include(${CMAKE_SCRIPT_DIR}/third-party-libs.cmake)
include(${CMAKE_SCRIPT_DIR}/compilation.cmake)
