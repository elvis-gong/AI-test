cmake_minimum_required(VERSION 3.16)

find_package(ASC REQUIRED)

project(sqrt_softplus_top_k_custom LANGUAGES ASC CXX)

set(CMAKE_CXX_STANDARD 14)

if(DEFINED NPU_ARCH)
    set(SOC_ARCH ${NPU_ARCH})
else()
    set(SOC_ARCH "dav-2201")
endif()

add_executable(sqrt_softplus_top_k_custom main.asc)

target_link_libraries(sqrt_softplus_top_k_custom PRIVATE
    tiling_api
    register
    platform
    unified_dlog
    dl
    m
    graph_base
)

target_include_directories(sqrt_softplus_top_k_custom PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_options(sqrt_softplus_top_k_custom PRIVATE
    $<$<COMPILE_LANGUAGE:ASC>:--npu-arch=${SOC_ARCH}>
)
