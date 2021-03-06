#!/usr/bin/env python3

import os
import os.path
import subprocess
import sys
from typing import List


PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def update_single_test(folder: str) -> None:
    log_folder = folder

    current_folder = os.curdir  # type: str
    os.chdir("{0}/{1}".format(PROJECT_FOLDER, folder))

    update_jenny_execution(log_folder,
                           "jenny-expected.txt")
    update_jenny_execution(log_folder,
                           "jenny-expected-info.txt",
                           ["--info"])

    os.chdir(current_folder)


def update_jenny_execution(log_folder: str,
                           log_file_name: str,
                           extra_arguments: List[str] = None) -> None:
    if not extra_arguments:
        extra_arguments = []

    print("Updating %s (%s)" % (log_folder, " ".join(extra_arguments)))

    expected_file = "{0}/{1}".format(log_folder, log_file_name)
    popen_command = ["%s/jenny" % PROJECT_FOLDER]
    popen_command.extend(extra_arguments)

    with open("{0}/{1}".format(PROJECT_FOLDER, expected_file),
              mode="w") as output_file:
        status, output = subprocess.getstatusoutput(" ".join(popen_command))
        print(output)

        if status != 0 and 'fail' not in log_folder:
            raise Exception("Wrong return code: %d" % status)

        output_file.write(output + "\n")


tests_to_run = [
    "features/ansiColor-support",
    "features/credentials-in-container",
    "features/archiveArtifacts",
    "features/testset/parent",
    "features/multiple-nodes",
    "features/child-section-skip/parent",
    "features/dir-step",
    "features/different-work-folder/parent",
    "features/failing-project",
    "features/failing-sh-inside-docker",
    "features/mock-missing-functions",
    "features/current-build",
    "features/external-classes",
    "features/build_id-environment-variable",
    "features/stash-unstash",
    "features/docker-user-id-inside",
    "features/docker-support",
    "features/junit-support"
]

if len(sys.argv) > 1:
    tests_to_run = sys.argv[1:]

for test in tests_to_run:
    update_single_test(test)
