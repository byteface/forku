"""
    forku
    ====================================

    If you patch a python lib in your local virtual env. 
    forku ("fork you") tries to fork the repo and apply the patch.

    This only works if a repo can be found for that library.

    It currently makes a lot of assumption, so wont work for many cases.

        -- assumes git
        -- assumes latest version of lib. Careful. if not this could result in reverting the target lib.
        -- assumes you have virtualenv
        -- assumes you are in the correct directory
        -- assume a dist-info folder exists with METADATA with a Home-page
        -- assumes you have a github account
        -- assumes you have gh cli installed
        -- assumes os?? not sure

    See README.md for more information.

    # TODO -
        - add support for other git repos like bitbucket
        - add support for other python libs
        - add support for other os
        - add support for other packing systems

"""

__version__ = "0.0.2"
__license__ = 'MIT'
__author__ = "@byteface"

VERSION = __version__

import requests
import re
import os
import sys
import subprocess
import json
import time

class forku:

    DEFAULT_VENV = "venv/lib/python3.9/site-packages/"
    # DEFAULT_VENV_PC = "venv\\lib\\python3.9\\site-packages\\"

    DEFAULT_REQUIREMENTS = 'requirements.txt'

    @staticmethod
    def run(library: str):
        if not library:
            print("Please provide a library name")
            return
        
        # find the libary in the virtual env
        lib_path = forku.get_library_path(library)
        if not lib_path:
            print("No library found")
            return

        print("Library Found:", lib_path)

        # get the url to the repo for said libary
        github_url = forku.get_github_url(library)
        if not github_url:
            print("No github url found")
            return

        # fork github repo and push the changes to the fork
        cloned_repo_folder = forku.fork_repo(github_url)

        # if fork fails clone the existing fork - NOTE - gh cli does this
        # cloned_repo_folder = forku.clone_repo(github_fork_url)

        # move the changed files in the library into the cloned repo
        forku.copy_accross_changed_files(library, lib_path, cloned_repo_folder)

        # check the changes and ask the user to confirm they are happy
        if not forku.confirm_changes(cloned_repo_folder):
            print("Your changes were applied but not committed.")
            return
        # create a new branch and commit the changes
        forku.branch_and_commit_changes(cloned_repo_folder)

        # push the changes to the fork
        forku.push_changes(cloned_repo_folder)

        # create a pull request
        forku.create_pull_request(github_url)
        print("Done")


    @staticmethod
    def get_library_path(library: str):
        """
        returns the full path of the library if it can be found
        """
        import os
        import glob
        import sys

        # get the current working directory
        cwd = os.getcwd()

        # join it to the DEFAULT_VENV
        venv_path = os.path.join(cwd, forku.DEFAULT_VENV)
        # print(venv_path)

        # print(library)
        # get the folder names in venv_path that contain word in the lib
        folders = glob.glob(os.path.join(venv_path, "*" + library + "*"))
        # print(folders)

        # dont return the one that contain dist-info
        folders = [x for x in folders if not "dist-info" in x]
        # print(folders)

        # if there is more than one folder, ask the user to select one
        selection = None
        if len(folders) > 1:
            print("Multiple libraries found that might match")
            for i, folder in enumerate(folders):
                print(f"{i} - {folder}")

            import builtins
            selection = builtins.input("Please select one: ")
            # selection = input("Please select one: ")
            selection = folders[int(selection)]
        elif len(folders) == 1:
            selection = folders[0]
        
        # if there is no folder, return None
        if not selection:
            print("No library found")
            return None

        # return the full path of the folder
        return selection


    @staticmethod
    def get_github_url(library: str):
        """
        returns the github url of the library
        """
        import os
        import glob
        import sys

        # get the current working directory
        cwd = os.getcwd()

        # join it to the DEFAULT_VENV
        venv_path = os.path.join(cwd, forku.DEFAULT_VENV)
        folders = glob.glob(os.path.join(venv_path, "*" + library + "*"))
        # print(folders)

        # only keep the ones that contain dist-info
        folders = [x for x in folders if "dist-info" in x]
        # print(folders)

        # if there is more than one folder, ask the user to select one
        selection = None
        if len(folders) > 1:
            print("Multiple libraries found that might match")
            for i, folder in enumerate(folders):
                print(f"{i} - {folder}")

            import builtins
            selection = builtins.input("Please select one: ")
            # selection = input("Please select one: ")
            selection = folders[int(selection)]
        elif len(folders) == 1:
            selection = folders[0]

        # if there is no folder, return None
        if not selection:
            print("No info for the library could be found.")
            # TODO - search on github
            return None

        # TODO - Project-URL: Source, https://github.com/psf/requests
        # TODO - better to just regex whole file for urls?
        # get the METADATA file and extract the homepage
        with open(os.path.join(selection, "METADATA"), "r") as f:
            print('sup!!!')
            # for line in f:
            #     if "Home-page" in line:
            #         line = line.split(" ")
            #         return line[-1].strip()
            url = forku._get_github_url(f.read())
            
            print(url)

            return url
        
        # if there is no homepage, return None
        print("No homepage found")
        return None


    @staticmethod
    def clone_repo(github_url: str):
        """
        clones the repo to a temp folder in the current working directory
        """
        # get the folder name from teh github url
        folder_name = github_url.split("/")[-1]

        # create a new folder in the current working directory
        current_dir = os.getcwd()
        tmp_dir = os.path.join(current_dir, folder_name)
        os.mkdir(tmp_dir)

        # clone the repo to the temp folder
        # os.system(f"git clone {github_url} {folder_name}")
        # DONT use os.system
        import subprocess
        subprocess.call(["git", "clone", github_url, folder_name])

        # return the full path of the temp folder
        return folder_name


    @staticmethod
    def fork_repo(repo_url: str):
        """
        forks the repo using gh cli
        """
        # get the folder name from teh github url
        folder_name = repo_url.split("/")[-1]

        # os.system(f"gh repo fork {repo_url} --clone=true")
        import subprocess
        subprocess.call(["gh", "repo", "fork", repo_url, "--clone=true"])

        return folder_name


    @staticmethod
    def copy_accross_changed_files(lib_name:str, lib_path: str, cloned_repo_folder: str):
        """
        copies the changed files in the library into the cloned repo
        """
        import os
        import shutil

        # copy all python files in the lib_path to the lib_name folder in the cloned repo
        for file in os.listdir(lib_path):
            if file.endswith(".py"):
                shutil.copy(os.path.join(lib_path, file), os.path.join(cloned_repo_folder, lib_name))


    @staticmethod
    def confirm_changes(cloned_repo_folder: str):
        """ do a git status and ask the user if they are happy with the changes """

        diff = subprocess.check_output(["git", "diff"], cwd=cloned_repo_folder)
        print(diff.decode("utf-8"))

        # get the status of the repo
        status = subprocess.check_output(["git", "status"], cwd=cloned_repo_folder)
        print(status.decode("utf-8"))

        # ask the user if they are happy with the changes
        import builtins
        selection = builtins.input("Are you happy with the changes? (y/n) ")
        # selection = input("Are you happy with the changes? (y/n) ")
        if selection.lower() == "y":
            return True
        else:
            return False

    
    @staticmethod
    def branch_and_commit_changes(cloned_repo_folder: str):
        """
        creates a new branch and commits the changes
        """
        # create a new branch
        subprocess.call(["git", "checkout", "-b", "forku"], cwd=cloned_repo_folder)

        # ask the user to input a commit message
        import builtins
        message = builtins.input("Enter a commit message: ")
        message = message + " (forku)"

        # add and commit the changes
        subprocess.call(["git", "add", "."], cwd=cloned_repo_folder)
        subprocess.call(["git", "commit", "-m", message], cwd=cloned_repo_folder)


    @staticmethod
    def push_changes(cloned_repo_folder: str):
        """
        pushes the changes to the remote repo
        """
        # push the changes
        subprocess.call(["git", "push", "origin", "master"], cwd=cloned_repo_folder)


    @staticmethod
    def create_pull_request():
        """
        creates a pull request
        """
        # TODO - create a pull request
        pass


    @staticmethod
    def _get_github_url(somestring: str):
        """
        returns the github url of the library
        """
        import re
        url = re.search(r"https?://github.com/[\w-]+/[\w-]+", somestring)
        if url:
            return url.group()
        else:
            return None


    @staticmethod
    def _check_if_installed_library_is_same_as_github():
        """
        checks if the library is the same as the github repo
        """
        # TODO - check if the library is the same as the github repo
        return True


    @staticmethod
    def githubify_requirements(requirements:str = None):
        """
        github files the requirements.txt file
    
        by changing all the libary names to the github url. (can't pip or something already do this?)

        https://stackoverflow.com/questions/13685920/install-specific-git-commit-with-pip

        would need to get the tag or revision for each lib. add user changes then rebase changes from pulled

        """

        if requirements is None or isinstance(requirements, bool):
            requirements = forku.DEFAULT_REQUIREMENTS
        
        # create a new file
        with open("github-" + requirements, "w") as f:
            # for each line in the requirements file
            for line in open(requirements, "r"):
                # if the line is a library
                if "==" in line:
                    # get the library name
                    lib_name = line.split("==")[0].strip()
                    # get the github url
                    github_url = forku.get_github_url(lib_name)
                    # if there is a github url
                    if github_url:
                        # change the line to the github url
                        line = line.replace(lib_name, github_url)
                # write the line to the new file
                f.write(line)
        
        # return the contents of the new file
        with open("github-" + requirements, "r") as f:
            return f.read()
