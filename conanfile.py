from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import shutil
import os


class XtensorioConan(ConanFile):
    name = "xtensor-io"
    version = "0.4.0"
    license = "BSD-3"
    url = "https://github.com/darcamo/conan-xtensor-io"
    description = "xtensor plugin to read and write images, audio files and numpy (compressed) npz "
    no_copy_source = True
    homepage = "https://github.com/QuantStack/xtensor-io"
    generators = "cmake"
    # No settings/options are necessary, this is header only

    def system_requirements(self):
        if tools.os_info.is_linux:
            installer = tools.SystemPackageTool()
            if tools.os_info.linux_distro == "arch":
                installer.install("openimageio")
                installer.install("libsndfile")
                installer.install("zlib")
                installer.install("freetype2")
            else:
                raise ConanException("Don't know package name for other distros")
        else:
            raise ConanException("Implement-me")

    def requirements(self):
        self.requires("xtensor/0.16.4@darcamo/stable")
        self.requires("xtl/0.4.12@darcamo/stable")

    def source(self):
        tools.get("https://github.com/QuantStack/xtensor-io/archive/{0}.zip".format(self.version))
        shutil.move("xtensor-io-{0}".format(self.version), "sources")

        tools.replace_in_file("sources/CMakeLists.txt", "project(xtensor-io)",
                              """project(xtensor-io)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["OpenImageIO", "sndfile", "z"]
