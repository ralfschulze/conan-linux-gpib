import os

from conans import ConanFile, CMake, tools


class LinuxGpibTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):

        # Get 'gpib.conf' from 'linux-gpib' package folder to prevent error
        # about missing 'gpib.conf'.
        pkg_folder = self.deps_cpp_info["linux-gpib"].rootpath

        if not tools.cross_building(self):
            with tools.environment_append(
                {"IB_CONFIG": "{p}/etc/gpib.conf".format(p=pkg_folder)}
            ):
                os.chdir("bin")
                self.run(".%sexample" % os.sep)
