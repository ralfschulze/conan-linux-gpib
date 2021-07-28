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
               "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    generators = "cmake"
    
    _autotools = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        url = "https://sourceforge.net/projects/linux-gpib/files/linux-gpib%20for%203.x.x%20and%202.6.x%20kernels/"\
            "{v}/linux-gpib-{v}.tar.gz".format(v=self.version)
        tools.get(url)
        tools.unzip(
            "linux-gpib-{v}/linux-gpib-user-{v}.tar.gz".format(v=self.version), strip_root=True)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        args = []
        args.append("--disable-all-bindings")

        if self.options.shared:
            args.append("--enable-shared")
            args.append("--disable-static")
        else:
            args.append("--disable-shared")
            args.append("--enable-static")

        self._autotools = AutoToolsBuildEnvironment(self)
        self._autotools.fpic = self.options.fPIC
        self._autotools.configure(args=args)
        
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
