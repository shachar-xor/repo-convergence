
include(${CMAKE_SCRIPT_DIR}/conan.cmake)

conan_cmake_run(CONANFILE      ${CONAN_DIR}/conanfile.txt
                INSTALL_FOLDER ${THIRD_PARTY_LIBS_DIR}
                REMOTE         catotest
                PROFILE        ${CONAN_DIR}/profiles/${CONFIGURATION_NAME}.ini
                BUILD          missing)

conan_basic_setup()
