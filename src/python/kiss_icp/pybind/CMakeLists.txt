pybind11_add_module(kiss_icp_pybind MODULE kiss_icp_pybind.cpp)
target_link_libraries(kiss_icp_pybind PRIVATE kiss_icp::core kiss_icp::metrics)
install(TARGETS kiss_icp_pybind DESTINATION .)
