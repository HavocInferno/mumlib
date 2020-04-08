from conans import ConanFile, CMake, tools


class mumlibConan(ConanFile):
    name = "mumlib"
    version = "1.0.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of PostOffice here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = ( ("boost/1.67.0@conan/stable"), ("OpenSSL/1.0.2l@conan/stable") )

    def source(self):
        self.run("git clone https://github.com/hiro2233/mumlib.git")
        self.run("cd mumlib && git checkout master")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="mumlib")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="mumlib/include", keep_path=False)
        self.copy("*mumlib.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mumlib"]

