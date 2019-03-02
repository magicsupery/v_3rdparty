import yaml
import sys
import os
import shutil


SOURCE_DIR = "source"
LOG_DIR = "log"
BUILD_DIR = "build"

SOURCE_DIR = os.path.realpath(SOURCE_DIR)
BUILD_DIR = os.path.realpath(BUILD_DIR)


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def create_empty_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)


create_dir(SOURCE_DIR)
create_dir(LOG_DIR)
create_dir(BUILD_DIR)


def run_cmd(cmd):
    os.system(cmd)
    print cmd


class Builder(object):
    def __init__(self, info, target=None):
        self.info = info
        self.ninja = None

    def build_ninja(self):
        source_dir = os.path.join(SOURCE_DIR, "ninja")
        build_dir = os.path.join(BUILD_DIR, "ninja")

        suffix = ""

        # suffix = "" if cfg.BUILD_OS == "osx" else ".exe"
        self.ninja = os.path.join(build_dir, "ninja%s"%(suffix, ))
        if os.path.exists(self.ninja):
            print '================== Ninja Alredy Build, Skipped... =================='
            return
        
        create_empty_dir(build_dir)

        cmd = "cd %s && python %s/configure.py --bootstrap"%(build_dir, source_dir)
        run_cmd(cmd)

    def clean(self):
        

    def build_one_lib(self, lib_name, cmake_dir, cmake_args=None):
        source_dir = os.path.join(SOURCE_DIR, lib_name)
        build_dir = os.path.join(BUILD_DIR, lib_name)
        install_dir = os.path.realpath(self.info.get("install", "install"))

        create_empty_dir(build_dir)

        now_path = os.path.realpath(".")
        os.chdir(build_dir)
        
        print '================== BUILD %s BEGIN =================='%(lib_name.upper(), )
        final_cmake_args = []
        final_cmake_args.extend(self.info.get("cmake_args", []))
        if cmake_args:
            final_cmake_args.extend(cmake_args)
        final_cmake_args.append("-DCMAKE_INSTALL_PREFIX=%s"%(install_dir,))
        final_cmake_args.append("-DCMAKE_MAKE_PROGRAM=%s"%self.ninja)
        
        cmake_arg_str = " ".join(final_cmake_args)
        cmd = " ".join(["cmake -G Ninja", cmake_arg_str, "%s/%s"%(source_dir, cmake_dir)])
        
        run_cmd(cmd)
        run_cmd(self.ninja)
        run_cmd(self.ninja + " install")
        print '================== BUILD %s END =================='%(lib_name.upper(), )

        os.chdir(now_path)


    def build_libs(self):
        for name, attr in self.info["depends"].items():
            if name == "ninja":
                continue
            self.build_one_lib(name, "")


    def download_libs(self):
        for name, attr in self.info["depends"].items():
            git_url = attr.get("git", None)
            if git_url:
                source_path = os.path.join(SOURCE_DIR, name)
                if not os.path.exists(source_path):
                    run_cmd("cd %s && git clone %s %s"%(SOURCE_DIR, git_url, name))
                else:
                    run_cmd("cd %s && git pull"%(source_path, ))
            

    def work(self):
        self.download_libs()
        self.build_ninja()
        self.build_libs()


if __name__ == "__main__":
    with open("depends.yaml") as f:
        try:
            info = yaml.load(f)
        except yaml.YAMLError as e:
            print e

        print  info
        Builder(info).work()