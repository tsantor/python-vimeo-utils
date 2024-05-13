# Python Vimeo Utils

![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

## Overview

Wrapper functions around pyvimeo for common interactions with the Vimeo SDK with sane `fields` defaults. Vimeo loves to return **overly verbose** responses.

## Installation

Install Python Vimeo Utils:

```bash
python3 -m pip install python-vimeo-utils
```

## Usage
```python
import vimeo_utils

vclient = vimeo.VimeoClient(
    token="VIMEO_ACCESS_TOKEN",
    key="VIMEO_CLIENT_ID",
    secret="VIMEO_CLIENT_SECRET",
)

vimeo_utils.get_video_info(vclient, '/videos/1234567890')
```

<!-- ## Documentation
Visit the docs [here](https://github.io/tsantor/python-vimeo-utils/docs) -->

## Development
To get a list of all commands with descriptions simply run `make`.

```bash
make env
make pip_install
make pip_install_editable
```

## Testing

```bash
make pytest
make coverage
make open_coverage
```

## Deploying

```bash
# Publish to PyPI Test before the live PyPi
make release_test
make release
```

## Issues

If you experience any issues, please create an [issue](https://github.com/tsantor/python-vimeo-utils/issues) on Github.
