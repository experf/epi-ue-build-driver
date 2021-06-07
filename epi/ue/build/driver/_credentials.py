"""Loading SSL credentials for gRPC Python authentication example."""

import os


def _load_credential_from_file(filepath, binary=False, strip=False):
    real_path = os.path.join(os.path.dirname(__file__), "credentials", filepath)
    mode = "rb" if binary else "r"
    with open(real_path, mode) as f:
        contents = f.read()
        if strip:
            return contents.strip()
        return contents

PASSWORD_HEADER_KEY = "x-password"
SERVER_CERTIFICATE = _load_credential_from_file('service.pem', binary=True)
SERVER_CERTIFICATE_KEY = _load_credential_from_file('service.key', binary=True)
ROOT_CERTIFICATE = _load_credential_from_file('ca.cert', binary=True)
PASSWORD = _load_credential_from_file("password.txt", strip=True)
