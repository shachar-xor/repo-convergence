set(CMAKE_MINIMUM_VERSION "3.19.0")
set(LANGUAGES "C;CXX")
set(PROJECT_NAME "client")

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_VERSION})
project(${PROJECT_NAME} LANGUAGES ${LANGUAGES})

set(CMAKE_SCRIPT_DIR ${CMAKE_SOURCE_DIR}/common/cmake)
include(${CMAKE_SCRIPT_DIR}/setup.cmake)

add_subdirectory(common)

if (IS_LINUX OR IS_APPLE)
    add_subdirectory(linux)
elseif (IS_WINDOWS)
    add_subdirectory(windows)
endif()
