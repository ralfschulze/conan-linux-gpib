from conans import ConanFile, AutoToolsBuildEnvironment, tools


class LinuxGpibConan(ConanFile):
    name = "linux-gpib"
    version = "4.3.4"
    license = "GPLv2"
    author = "Ralf Schulze <ralf.schulze@gmx.net>"
    url = "https://github.com/ralfschulze/conan-linux-gpib"
    description = "Linux GPIB driver library"
    topics = ("linux", "gpib", "driver")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "static": [True, False],
               "fPIC": [True, False]}
    default_options = {"shared": True, "static": False, "fPIC": True}
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        url = "https://sourceforge.net/projects/linux-gpib/files/linux-gpib%20for%203.x.x%20and%202.6.x%20kernels/"\
            "{v}/linux-gpib-{v}.tar.gz".format(v=self.version)
        tools.get(url)
        tools.unzip(
            "linux-gpib-{v}/linux-gpib-user-{v}.tar.gz".format(v=self.version), strip_root=True)

    def build(self):
        args = []
        args.append("--disable-all-bindings")

        if self.options.shared:
            args.append("--enable-shared")
        else:
            args.append("--disable-shared")
    
        if self.options.static:
            args.append("--enable-static")
        else:
            args.append("--disable-static")

        autotools = AutoToolsBuildEnvironment(self)
        autotools.fpic = self.options.fPIC
        autotools.configure(args=args)
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
