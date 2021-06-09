# pylint: disable=global-statement

import argparse
from subprocess import check_output, run
from os.path import join, exists
import requests
from xml.etree import ElementTree

from ue4helpers import ProjectPackager


class OurProjectPackager(ProjectPackager):
    """
    Just to make it clear what we're adding to the `ue4-ci-helpers` stuff --
    basically just acessing private data.
    """

    @property
    def archive_root(self):
        """
        The final product archive "root" -- the `base_name` argument to
        `shutil.make_archive()`. The archive filename, without archive
        extension(s).
        """
        return join(self._root, self._archive)

    def archive_path(self, extension):
        return f"{self.archive_root}.{extension}"


def parse_args():
    parser = argparse.ArgumentParser(description="Build UE4 projects")
    parser.add_argument(
        "--repo_name",
        help="What to call the repo in PlasticSCM (I guess?)",
        required=True,
    )
    parser.add_argument(
        "--repo_src",
        help="PlasticSCM repo to clone from",
        required=True,
    )
    parser.add_argument(
        "--repo_root",
        help="Where to put the repo",
        required=True,
    )
    parser.add_argument(
        "--project_root",
        help=(
            "Directory project lives in (usually a sub-directory of repo_root)"
        ),
        required=True,
    )
    parser.add_argument(
        "--put_to",
        help="URL to PUT the result",
        required=True,
    )
    parser.add_argument(
        "--engine_root",
        help="Where the engine directory is",
        required=True,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    clone_repo(
        repo_name=args.repo_name,
        repo_src=args.repo_src,
        repo_root=args.repo_root,
    )
    set_ue4cli_root(engine_root=args.engine_root)
    archive_path = package(
        repo_root=args.repo_root, project_root=args.project_root
    )
    print(f"SUCCESS {archive_path}")
    # upload(args.put_to, archive_path)


def clone_repo(repo_name: str, repo_src: str, repo_root: str):
    if not exists(repo_root):
        run(
            [
                "cm",
                "workspace",
                "create",
                repo_name,
                repo_root,
                f"--repository={repo_src}",
            ],
            check=True,
            capture_output=True,
        )
    run(["cm", "update"], cwd=repo_root, check=True, capture_output=True)


def set_ue4cli_root(engine_root):
    run(["ue4", "setroot", engine_root], check=True, capture_output=True)


def get_version(repo_root) -> str:
    status_result = run(
        ["cm", "status", "--xml"],
        cwd=repo_root,
        encoding="utf-8",
        check=True,
        capture_output=True,
    )
    status_output = ElementTree.fromstring(status_result.stdout)

    changeset = (
        status_output.find("WorkspaceStatus")
        .find("Status")
        .find("Changeset")
        .text
    )

    return f"cs{changeset}"


def package(repo_root: str, project_root: str) -> str:
    # Create our project packager
    packager = OurProjectPackager(
        # The root directory for the project
        # (This example assumes this script is in a subdirectory)
        root=project_root,
        # Use the date of the most recent git commit as our version string
        version=get_version(repo_root=repo_root),
        # The filename template for our generated .zip file
        archive="{name}-{version}-{platform}",
        # Don't strip debug symbols from the packaged build
        strip_debug=False,
        # Don't strip manifest files from the packaged build
        strip_manifests=False,
    )

    # Clean any previous build artifacts
    # packager.clean()

    # Package the project
    packager.package(args=["Development"])

    # Compress the packaged distribution
    # (The CI system can then tag the generated .zip file as a build artifact)
    packager.archive()

    return packager.archive_path(".zip")


def upload(put_to: str, archive_path: str):
    with open(archive_path, "rb") as file:
        requests.put(put_to, data=file)


if __name__ == "__main__":
    main()
