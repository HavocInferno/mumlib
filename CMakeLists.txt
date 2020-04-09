cmake_minimum_required(VERSION 3.7)
project(mumlib)

####################################################################################
# CONAN & UCM
####################################################################################
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if ( NOT ${CMAKE_SYSTEM_NAME} STREQUAL "Linux" )
include( ucm )
add_definitions( /bigobj )
endif()
####################################################################################

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

if (NOT APPLE)
  add_definitions(-DOPT_TLS_GNUTLS -D_POSIX_C_SOURCE=200112L)
else()
  LINK_DIRECTORIES(/opt/local/lib) # Include the default MacPorts library directory
endif()

####################################################################################
# Protobuf manually
set(PROTOBUF_ROOT "C:/projects/Tryouts/protobuf/install")
include(${PROTOBUF_ROOT}/cmake/protobuf-config.cmake)
include(${PROTOBUF_ROOT}/cmake/protobuf-module.cmake)
include(${PROTOBUF_ROOT}/cmake/protobuf-options.cmake)
include(${PROTOBUF_ROOT}/cmake/protobuf-targets.cmake)
####################################################################################

INCLUDE(FindPkgConfig)
find_package(PkgConfig REQUIRED)
find_package(Boost COMPONENTS system REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(Protobuf REQUIRED HINTS ${PROTOBUF_ROOT}/cmake) # manually give Protobuf hint

pkg_check_modules(LOG4CPP "log4cpp")
pkg_check_modules(OPUS "opus")
####################################################################################
# Opus manually
set(OPUS_INCLUDE_DIRS "C:/projects/Tryouts/opus/opus-1.3.1-minimal/include")
#set(OPUS_LIBRARIES "") which libs does opus even need?...
####################################################################################

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
include_directories(${OPENSSL_INCLUDE_DIR})
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${OPUS_INCLUDE_DIRS})
set(SPEEXDSP_INCLUDE_DIRS "C:/projects/Tryouts/speex/speex-1.2.0-minimal/speexDSP/include")
include_directories(${SPEEXDSP_INCLUDE_DIRS})

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${LOG4CPP_INCLUDE_DIRS})

include_directories(include)

set(MUMLIB_PUBLIC_HEADERS include/mumlib.hpp include/mumlib/VarInt.hpp)

set(MUMLIB_PRIVATE_HEADERS
        include/mumlib/Callback.hpp
        include/mumlib/CryptState.hpp
        include/mumlib/Transport.hpp
        include/mumlib/Audio.hpp
        include/mumlib/enums.hpp
        )

set(MUMLIB_SRC
        src/mumlib.cpp
        src/Callback.cpp
        src/CryptState.cpp
        src/VarInt.cpp
        src/Transport.cpp
        src/Audio.cpp
        )

set(SPEEX_LIBRARIES
        C:/projects/Tryouts/speex/speex-1.2.0-minimal/speex/lib/x64/Debug/speex.lib
        C:/projects/Tryouts/speex/speex-1.2.0-minimal/speexDSP/lib/x64/Debug/speexdsp.lib
        )

PROTOBUF_GENERATE_CPP(PROTO_SRCS PROTO_HDRS Mumble.proto)

add_library(mumlib STATIC ${MUMLIB_SRC} ${MUMLIB_PUBLIC_HEADERS} ${MUMLIB_PRIVATE_HEADERS} ${PROTO_SRCS} ${PROTO_HDRS})

##### Conan
target_link_libraries(mumlib ${CONAN_LIBS})
#####
target_link_libraries(mumlib 
        ${SPEEX_LIBRARIES}
        ${PROTOBUF_LIBRARIES}
        ${Boost_LIBRARIES}
        ${OPENSSL_LIBRARIES}
        ${LOG4CPP_LIBRARIES}
        ${OPUS_LIBRARIES})

set_target_properties(mumlib PROPERTIES PUBLIC_HEADER "${MUMLIB_PUBLIC_HEADERS}")

add_executable(mumlib_example mumlib_example.cpp)
target_link_libraries(mumlib_example mumlib ${CONAN_LIBS})

install(TARGETS mumlib DESTINATION lib PUBLIC_HEADER DESTINATION include/mumlib) #just DESTINATION instead of LIBRARY DESTINATION for Win Cmake

############################################
if ( ${CMAKE_CXX_COMPILER_ID} STREQUAL MSVC )
ucm_set_runtime( STATIC )
endif()
############################################ 
