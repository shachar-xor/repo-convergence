# Repository Convergence

## Overview 

This repo comes along-side "Repo Convergence" presentation.

This repo was created to demostrate a monorepo of a c/c++ multi-platform project, and other topics talked about in the presentation.

The power-point file of the presentation is in the repository, [click here to download it](https://github.com/shachar-xor/repo-convergence/raw/main/Repo_Convergence.pptx)

## Compilation instructions

To compile, the following need to be installed in your system:

1. Install Python
2. Install CMake
3. Install conan
4. Install OS-specific compiler/IDE:
   - Windows - Visual Studio 2017
   - Linux - gcc/g++
   - Mac - XCode/Clang

## Folder Structure

| Link  | Desc |
| ------------- | ------------- |
| [windows/](windows)  | Windows specific files |
| [linux/](linux)  | Linux (and Mac) specifiec files |
| [common/](common)  | Common files |
| [common/lib/](common/lib)  | Common library |
| [common/cmake/](common/cmake)  | CMake related files |
| [common/conan/](common/conan)  | Conan related files |
| [build_all.py](build_all.py)  | Helper script to make build more standartized across diffrenet platforms  |
| `build_dir/`  | Build dirs and temporary files. This path is ignored by git |

# Topics

## Git subtree

Git subtree is not really demostrated here. 

Assuming we had a `windows-client` repository, this is how we would initially add it to the converged repo (to [windows/](windows) subdir):

```
git remote add window-client https://github.com/shachar-xor/windows-client.git
git fetch window-client
git subtree add --prefix windows window-client main
```

If we would want to merge changes from `windows-client` repository back to this repo:

```
git fetch window-client
git pull –s subtree windows windows-repo master
```

## CMake

The `CMakeLists.txt` files are scattered across the repo. Some interesting files are:

 - [CMakeLists.txt](CMakeLists.txt) - The main cmake file
 - [common/cmake/](common/cmake/) - CMake scripts, where the setup of cmake is taking place
 - [common/lib/CMakeLists.txt](common/lib/CMakeLists.txt) - CMake of the common library
 - [common/lib/ut/CMakeLists.txt](common/lib/ut/CMakeLists.txt) - CMake of the common unit-tests
 - [linux/CMakeLists.txt](linux/CMakeLists.txt) - CMake of linux-specific project

## Conan

 - [common/conan/](common/conan) - Conan profiles
 - [common/cmake/conan.cmake](common/cmake/conan.cmake) - CMake wrapper for Conan, taken from [github.com/conan-io/cmake-conan](https://github.com/conan-io/cmake-conan)
 - [common/cmake/third-party-libs.cmake](common/cmake/third-party-libs.cmake) - Using the Conan wrapper

## build_all Script

[build_all.py](build_all.py) is a helper script, to make build easier and more standart across diffrenet platforms

For example, if you run the script from Windows, you'll see:
    
       - Current working dir: C:\workspace\repo-conv\repo-conv-temp
       - Current logging dir: build_dir\build_all_script\logs\2022-06-12_21-59-50
       - is_verbose: False
       - configurations: ['win32-debug', 'win32-release', 'win64-debug', 'win64-release']
       - steps: ['clean', 'cmake', 'nuget', 'build', 'test']
       - project_version: None

      win32-debug/clean-> cmd: if exist build_dir\win32-debug rmdir /s /q build_dir\win32-debug
      win32-debug/clean-> SUCCESS!
      win32-debug/cmake-> cmd: cmake -S . -B build_dir\win32-debug -G "Visual Studio 15 2017" -D CMAKE_BUILD_TYPE=Debug -A win32 -D BUILD_MODE:STRING=Debug
      win32-debug/cmake-> SUCCESS!
      win32-debug/nuget-> cmd: build_dir\build_all_script\nuget.exe restore build_dir\win32-debug
      win32-debug/nuget-> SUCCESS!
      win32-debug/build-> cmd: cmake --build build_dir\win32-debug  --config Debug --target ALL_BUILD
      win32-debug/build-> SUCCESS!
      win32-debug/test-> cmd: cmake --build build_dir\win32-debug  --config Debug --target RUN_TESTS
      win32-debug/test-> SUCCESS!
      win32-release/clean-> cmd: if exist build_dir\win32-release rmdir /s /q build_dir\win32-release
      win32-release/clean-> SUCCESS!
      win32-release/cmake-> cmd: cmake -S . -B build_dir\win32-release -G "Visual Studio 15 2017" -D CMAKE_BUILD_TYPE=Release -A win32 -D BUILD_MODE:STRING=Release
      win32-release/cmake-> SUCCESS!
      win32-release/nuget-> cmd: build_dir\build_all_script\nuget.exe restore build_dir\win32-release
      win32-release/nuget-> SUCCESS!
       ...

By default, on Windows, `build_all.py` will build all 4 available configuration (`win32-debug`, `win32-release`...), 
and perform all 4 steps (`cmake`, `nuget`, `clean`, `build`, `test`).

The terminal command is printed for each config/step, so you can run them by yourself.

All output for each step is saved in `build_dir/build_all_script/logs/{datetime}/{cfg}/{step}.txt`

In case of error, the script will break current configuration and point to the relevant log file, for example:

    win32-debug/test-> cmd: cmake --build build_dir/win32-debug  --config Debug --target RUN_TESTS
    win32-debug/test-> FAILED!
    win32-debug/test-> You can view log here: build_dir\build_all_script\logs\2021-05-23_19-09-32\win32-debug\test_output.txt
    win32-debug -> Breaking because last step failed

The script have diffrenet configurations and might have diffrenet steps for each one of the platforms 
(Windows, Linux, Apple). 
To see the configurations/steps for the current platform, run `build_all.py -h`
