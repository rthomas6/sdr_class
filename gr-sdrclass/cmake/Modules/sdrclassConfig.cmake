INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SDRCLASS sdrclass)

FIND_PATH(
    SDRCLASS_INCLUDE_DIRS
    NAMES sdrclass/api.h
    HINTS $ENV{SDRCLASS_DIR}/include
        ${PC_SDRCLASS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SDRCLASS_LIBRARIES
    NAMES gnuradio-sdrclass
    HINTS $ENV{SDRCLASS_DIR}/lib
        ${PC_SDRCLASS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SDRCLASS DEFAULT_MSG SDRCLASS_LIBRARIES SDRCLASS_INCLUDE_DIRS)
MARK_AS_ADVANCED(SDRCLASS_LIBRARIES SDRCLASS_INCLUDE_DIRS)

