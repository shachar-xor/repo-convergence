#!/usr/bin/env python3

import subprocess
import os
import sys
import traceback
import argparse
from urllib import request
from typing import List
from datetime import datetime
import platform


def is_windows():
    return platform.system() == 'Windows'


def is_linux():
    return platform.system() == 'Linux'


def is_apple():
    return platform.system() == 'Darwin'


def get_configurations():
    if is_linux():
        return [
            'linux-release',
            'linux-debug'
        ]
    elif is_windows():
        return [
            'win32-debug',
            'win32-release',
            'win64-debug',
            'win64-release',
        ]
    elif is_apple():
        return [
            'apple-release',
            'apple-debug'
        ]
    else:
        raise Exception('Unknown system')


def get_steps():
    if is_linux():
        return [
            'clean',
            'cmake',
            'build',
            'test',
        ]
    elif is_apple():
        return [
            'clean',
            'cmake',
            'build',
            'test',
        ]
    elif is_windows():
        return [
            'clean',
            'cmake',
            'nuget',
            'build',
            'test',
        ]
    else:
        raise Exception('Unknown system')


def get_root_folder() -> str:
    return os.path.dirname(os.path.realpath(__file__))


class Builder:

    def __init__(self, configuration: str, steps: List[str], nuget_exec_path: str, log_folder: str, is_verbose: bool,
                 project_version: str):
        self.configuration = configuration

        self.log_folder = os.path.join(log_folder, configuration)
        os.makedirs(self.log_folder, exist_ok=True)

        self.steps_dict = self._prepare_steps_dict(nuget_exec_path)

        self.steps_to_do = steps
        self.is_verbose = is_verbose

        self.project_version = project_version

        self.my_env = os.environ.copy()

        if self.project_version is not None:
            self.my_env['PROJECT_VERSION'] = self.project_version

    def _prepare_steps_dict(self, nuget_exec_path):

        build_folder = os.path.join('build_dir', self.configuration)

        steps_dict = {}

        additional_cmake_arg = ''
        extra_flags_cmake_step = ''

        release_or_debug = self.configuration.split('-')[1]
        release_or_debug_pascal_case = 'Release' if release_or_debug == 'release' else 'Debug'

        if is_windows():
            x32_or_x64 = self.configuration.split('-')[0]

            relwithdebinfo_or_debug = 'RelWithDebInfo' if release_or_debug == 'release' else 'Debug'
            win32_or_x64 = 'win32' if x32_or_x64 == 'win32' else 'x64'

            generator = '"Visual Studio 15 2017"'

            extra_flags_cmake_step = f'-A {win32_or_x64} ' \
                                     f'-D BUILD_MODE:STRING={release_or_debug_pascal_case} '

            steps_dict['nuget'] = f'{nuget_exec_path} restore {build_folder}'

            additional_cmake_arg = f' --config {relwithdebinfo_or_debug}'

        elif is_linux():
            generator = '"Unix Makefiles"'
        elif is_apple():
            generator = 'Xcode'

        if is_linux():
            all_target_name = 'all'
            test_target_name = 'test'
            package_target_name = 'package'
        else:
            all_target_name = 'ALL_BUILD'
            test_target_name = 'RUN_TESTS'
            package_target_name = 'PACKAGE'

        if is_windows():
            steps_dict['clean'] = f'if exist {build_folder} rmdir /s /q {build_folder}'
        else:
            steps_dict['clean'] = f'rm -Rf {build_folder}'

        steps_dict['cmake'] = f'cmake ' \
                              f'-S . ' \
                              f'-B {build_folder} ' \
                              f'-G {generator} ' \
                              f'-D CMAKE_BUILD_TYPE={release_or_debug_pascal_case} ' \
                              f'{extra_flags_cmake_step}'

        steps_dict['build'] = f'cmake --build {build_folder} {additional_cmake_arg} --target {all_target_name}'
        steps_dict['package'] = f'cmake --build {build_folder} {additional_cmake_arg} --target {package_target_name}'
        steps_dict['test'] = f'cmake --build {build_folder} {additional_cmake_arg} --target {test_target_name}'

        return steps_dict

    def _run_command(self, cmd: str, log_filename: str) -> bool:

        if not self.is_verbose:
            fd = open(log_filename, 'w')
            stdout_pipe = fd
        else:
            stdout_pipe = sys.stdout

        try:

            p = subprocess.Popen(cmd,
                                 stdout=stdout_pipe,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 shell=True,
                                 env=self.my_env)

            timeout_in_minutes = 5

            p.communicate(timeout=timeout_in_minutes * 60)
            success = (p.returncode == 0)
        except Exception as ex:
            stdout_pipe.write('Python exception!\n')
            stdout_pipe.write(traceback.format_exc())
            success = False

        if not self.is_verbose:
            fd.close()

        return success

    def _do_step(self, step_name: str) -> bool:

        log_filename = os.path.join(self.log_folder, f'{step_name}_output.txt')

        print_prefix = f'{self.configuration}/{step_name}->'

        cmd = self.steps_dict[step_name]

        print(f'{print_prefix} cmd: {cmd}')

        success = self._run_command(cmd, log_filename)

        if success:
            print(f'{print_prefix} SUCCESS!')
        else:
            print(f'{print_prefix} FAILED!')
            print(f'{print_prefix} You can view log here: {log_filename}')

        return success

    def run(self):

        for step_name in self.steps_to_do:

            success = self._do_step(step_name)

            if not success:
                print(f'{self.configuration} -> Breaking because last step failed')
                return False

        return True


def get_command_line_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Output will be written to console instead of log-files')

    configurations = get_configurations()

    parser.add_argument('-c',
                        dest='cfgs',
                        choices=configurations,
                        nargs='+',
                        default=configurations,
                        help='Which configurations to run')

    steps = get_steps()

    parser.add_argument('-s',
                        dest='steps',
                        choices=steps,
                        nargs='+',
                        default=steps,
                        help='Which steps to run')

    parser.add_argument('--version',
                        help='Set the project version string. Should be in format of X.Y.Z (e.g. 0.2.1)')

    return parser.parse_args()


def run(configurations, steps, is_verbose, project_version):

    # This script should always run from the root folder
    os.chdir(get_root_folder())

    time_now_formatted = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    base_folder = os.path.join('build_dir', 'build_all_script')
    base_log_folder = os.path.join(base_folder, 'logs')
    current_log_folder = os.path.join(base_log_folder, time_now_formatted)
    nuget_exec_path = os.path.join(base_folder, 'nuget.exe')

    os.makedirs(current_log_folder, exist_ok=True)

    print(f' - Current working dir: {get_root_folder()}')
    print(f' - Current logging dir: {current_log_folder}')
    print(f' - is_verbose: {is_verbose}')
    print(f' - configurations: {configurations}')
    print(f' - steps: {steps}')
    print(f' - project_version: {project_version}')
    print('')

    if 'nuget' in steps:
        if not os.path.isfile(nuget_exec_path):
            print('nuget.exe is missing, Downloading...')
            request.urlretrieve('https://dist.nuget.org/win-x86-commandline/latest/nuget.exe', nuget_exec_path)
            print('download done!')

    result = True

    for cfg in configurations:
        builder = Builder(cfg, steps, nuget_exec_path, current_log_folder, is_verbose, project_version)
        if not builder.run():
            result = False

    return result


def main():

    args = get_command_line_args()

    result = run(args.cfgs, args.steps, args.verbose, args.version)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
