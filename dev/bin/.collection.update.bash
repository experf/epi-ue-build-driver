#!/usr/bin/env bash

# Common / useful `set` commands
set -Ee # Exit on error
set -o pipefail # Check status of piped commands
set -u # Error on undefined vars
# set -v # Print everything
# set -x # Print commands (with expanded vars)

REPO_ROOT="$(git rev-parse --show-toplevel)"

cd "${REPO_ROOT}/ansible"
ansible-galaxy collection build --force

cd "${REPO_ROOT}/dev"
ansible-galaxy collection install --force \
	"${REPO_ROOT}/ansible/experf-ue_build_driver-0.0.1.tar.gz"
