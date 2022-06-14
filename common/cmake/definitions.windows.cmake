
if (CMAKE_GENERATOR_PLATFORM STREQUAL "win32")
    set(x32x64 x32)
    set(win32x64 win32)
    set(win32win64 win32)
    set(IS_32_BIT true)
    set(IS_64_BIT false)
elseif (CMAKE_GENERATOR_PLATFORM STREQUAL "x64")
    set(x32x64 x64)
    set(win32x64 x64)
    set(win32win64 win64)
    set(IS_32_BIT false)
    set(IS_64_BIT true)
else()
    message(FATAL_ERROR "Invalid CMAKE_GENERATOR_PLATFORM value, should be win32 or x64")
endif()