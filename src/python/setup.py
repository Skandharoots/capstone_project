import subprocess
import os
from pathlib import Path

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        cwd = Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        pyenv_root = os.environ.get("PYENV_ROOT")

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DTRANSIT_INCLUDE_TESTS:BOOL=OFF",
        ]

        if pyenv_root is not None:
            cmake_args += [f"-DPYTHON_EXECUTABLE={pyenv_root}/shims/python"]

        build_args = ["--config", "Release", "--", "-j2"]

        env = os.environ.copy()

        self.announce("Running CMake prepare", level=3)
        subprocess.check_call(["cmake", cwd] + cmake_args, cwd=self.build_temp, env=env)

        self.announce("Building extensions")
        cmake_cmd = ["cmake", "--build", "."]
        subprocess.check_call(cmake_cmd, cwd=self.build_temp)

setup(
    name="kiss-icp",
    version="0.3.0",
    description="Simple yet effective 3D LiDAR-Odometry registration pipeline",
    long_description_content_type="text/markdown",
    author="Ignacio Vizzo",
    author_email="ignaciovizzo@gmail.com",
    url="https://github.com/PRBonn/kiss-icp",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords=["LiDAR", "Localization", "Odometry", "SLAM"],
    python_requires=">=3.7",
    install_requires=[
        "natsort",
        "numpy",
        "plyfile",
        "pydantic<2",
        "pyquaternion",
        "rich",
        "tqdm",
        "typer[all]>=0.6.0",
    ],
    extras_require={
        "all": [
            "open3d>=0.13",
            "ouster-sdk>=0.7.1",
            "pyntcloud",
            "PyYAML",
            "trimesh",
        ],
        "visualizer": [
            "open3d>=0.13",
        ],
    },
    packages=["kiss_icp"],
    entry_points={"console_scripts": ["kiss_icp_pipeline=kiss_icp.tools.cmd:run"]},
    ext_modules=[CMakeExtension("kiss_icp_pybind")],
    cmdclass=dict(build_ext=CMakeBuild),
)
