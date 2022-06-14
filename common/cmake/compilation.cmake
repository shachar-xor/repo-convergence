
set(CMAKE_CXX_STANDARD 11)

if (IS_WINDOWS)
    include(${CMAKE_SCRIPT_DIR}/compilation.windows.cmake)
elseif (IS_LINUX)
    include(${CMAKE_SCRIPT_DIR}/compilation.linux.cmake)
elseif (IS_APPLE)
    include(${CMAKE_SCRIPT_DIR}/compilation.apple.cmake)
endif()