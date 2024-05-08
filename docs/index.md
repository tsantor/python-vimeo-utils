# Python Vimeo Utils

Wrapper functions around pyvimeo for common interactions with the Vimeo SDK with sane `fields` defaults.

## Installation
```bash
python3 -m pip install python-vimeo-utils
```

## Quickstart

Eager to get started? This page gives a good introduction in how to get started with Python Vimeo Utils.

First, make sure that:

- Python Vimeo Utils is installed
- Python Vimeo Utils is up-to-date

Let’s get started with some simple examples. Begin by importing the Python Vimeo Utils module:

```python
import vimeo_utils
```

Now, let’s get the user details:

```python
vclient = vimeo.VimeoClient(
    token="VIMEO_ACCESS_TOKEN",
    key="VIMEO_CLIENT_ID",
    secret="VIMEO_CLIENT_SECRET",
)

user_details = vimeo_utils.get_user(vclient)
```

Now, we have a dict called `user_details`. We can get all the information we need from this object.
