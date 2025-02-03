from typing import Annotated

from fastapi import Path

PREFIX_REGEX_PATTERN = "^[0-9a-fA-F]{5}$"  # first 5 chars of password's hash
Prefix = Annotated[
    str,
    Path(  # /!\ only enforced on FastApi side
        description="5 first chars of a password hash",
        example="5c283",
        pattern=PREFIX_REGEX_PATTERN,
    ),
]
Password = str  # type alias for clarity
