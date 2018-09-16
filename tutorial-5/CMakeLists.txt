cmake_minimum_required(VERSION 3.5)

set(PROJECT_NAME
        tutorial-5)

project(${PROJECT_NAME})

set(CMAKE_CXX_FLAGS
        "${CMAKE_CXX_FLAGS} -std=c++11 -ldl")


if (NOT MONERO_DIR)
    set(MONERO_DIR ~/monero)
endif()

message(STATUS MONERO_DIR ": ${MONERO_DIR}")

set(MONERO_SOURCE_DIR ${MONERO_DIR}
        CACHE PATH "Path to the root directory for Monero")

# set location of monero build tree
set(MONERO_BUILD_DIR ${MONERO_SOURCE_DIR}/build/Linux/master/release/
        CACHE PATH "Path to the build directory for Monero")

set(MY_CMAKE_DIR "${CMAKE_CURRENT_LIST_DIR}/cmake"
        CACHE PATH "The path to the cmake directory of the current project")

list(APPEND CMAKE_MODULE_PATH "${MY_CMAKE_DIR}")

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} "${MONERO_BUILD_DIR}"
        CACHE PATH "Add Monero directory for library searching")




# find boost
find_package(Boost COMPONENTS
        system
        filesystem
        thread
        date_time
        chrono
        regex
        serialization
        program_options
        date_time
        REQUIRED)

# include boost headers
include_directories(
        ${Boost_INCLUDE_DIRS}
 )

include_directories(
		${MONERO_SOURCE_DIR}/src
		${MONERO_SOURCE_DIR}/external
		${MONERO_SOURCE_DIR}/build
		${MONERO_SOURCE_DIR}/external/easylogging++
		${MONERO_SOURCE_DIR}/contrib/epee/include
		${MONERO_SOURCE_DIR}/version
                ${MONERO_SOURCE_DIR}/external/db_drivers/liblmdb)


# Specific source files
set(SOURCE_FILES
        main.cpp)

# Make Executable
add_executable(${PROJECT_NAME}
        ${SOURCE_FILES})


set_target_properties(${PROJECT_NAME}
        PROPERTIES LINKER_LANGUAGE CXX)


set(LIBRARIES        
        wallet
        blockchain_db
        cryptonote_core
        cryptonote_protocol
        cryptonote_basic
        daemonizer
        cncrypto
        blocks
        lmdb
        ringct
        device
        common
        mnemonics
        epee
        easylogging
        device
        pcsclite
        sodium
	pcsclite
        ${Boost_LIBRARIES}
        pthread
        unbound
        crypto
	ringct_basic
        ssl)

if (Xmr_CHECKPOINTS_LIBRARIES)
    set(LIBRARIES ${LIBRARIES} checkpoints)
endif()

set(LIBS common;blocks;cryptonote_basic;cryptonote_core;
		cryptonote_protocol;daemonizer;mnemonics;epee;lmdb;device;
                blockchain_db;ringct;wallet;cncrypto;easylogging;version;
                checkpoints; ringct_basic; )

foreach (l ${LIBS})

	string(TOUPPER ${l} L)

	find_library(Xmr_${L}_LIBRARY
			NAMES ${l}
			PATHS ${CMAKE_LIBRARY_PATH}
			PATH_SUFFIXES "/src/${l}" "/src/ringct" "/src/" "/external/db_drivers/lib${l}" "/lib" "/src/crypto" "/contrib/epee/src" "/external/easylogging++/"
			NO_DEFAULT_PATH
			)

	set(Xmr_${L}_LIBRARIES ${Xmr_${L}_LIBRARY})

	message(STATUS " Xmr_${L}_LIBRARIES ${Xmr_${L}_LIBRARY}")

	add_library(${l} STATIC IMPORTED)
	set_property(TARGET ${l} PROPERTY IMPORTED_LOCATION ${Xmr_${L}_LIBRARIES})

endforeach()


target_link_libraries(${PROJECT_NAME} ${LIBRARIES})
