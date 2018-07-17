from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")
    # Header-only library, but the dependencies will only correctly link with c++11 API
    builder.add(settings={"compiler.libcxx": "libstdc++11"})
    builder.run()
