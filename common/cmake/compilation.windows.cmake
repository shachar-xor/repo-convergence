
# Forces only a single configuration in the solution (Debug or RelWithDebInfo)
set(CMAKE_CONFIGURATION_TYPES "${RELWITHDEBINFO_OR_DEBUG}" CACHE STRING "" FORCE)

set(CMAKE_DOTNET_TARGET_FRAMEWORK_VERSION "v4.6")
set(CMAKE_CSharp_FLAGS "/platform:anycpu")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /W3")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /MP")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /EHsc")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /FC")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /Zi")

if (IS_RELEASE_MODE)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /Gy")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /Oi")
endif()

set(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} /INCREMENTAL:NO")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zi")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W3")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /FC")

if (IS_RELEASE_MODE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /GL")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Gy")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Oi")
endif()

string(REPLACE "/INCREMENTAL" "/INCREMENTAL:NO" CMAKE_EXE_LINKER_FLAGS_DEBUG ${CMAKE_EXE_LINKER_FLAGS_DEBUG})
string(REPLACE "/INCREMENTAL" "/INCREMENTAL:NO" CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO ${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO})

if (IS_RELEASE_MODE)
    set(CMAKE_CXX_LINK_EXECUTABLE "${CMAKE_CXX_LINK_EXECUTABLE} /OPT:ICF")
endif()

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

if (IS_DEBUG_MODE)
    add_definitions(-D_DEBUG)
else()
    add_definitions(-DNDEBUG)
endif()

add_definitions(-D_CRT_SECURE_NO_WARNINGS)
add_definitions(-D_WINSOCK_DEPRECATED_NO_WARNINGS)
add_definitions(-D_LITTLE_ENDIAN)

