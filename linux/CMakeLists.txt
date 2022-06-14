set(TARGET_NAME ${CONFIGURATION_NAME}_client)

add_executable(${TARGET_NAME}
    main.cpp
)

target_link_libraries(${TARGET_NAME}
    lib
)

target_include_directories(${TARGET_NAME} PRIVATE ${COMMON_LIB_DIR})
