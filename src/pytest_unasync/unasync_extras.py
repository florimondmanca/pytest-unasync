"""Extra utilities built on top of unasync."""

import tokenize as std_tokenize
import typing

import unasync


def unasync_fileobj(f_in: typing.IO, f_out: typing.IO) -> None:
    """
    Generalized version of unasync.unasync_file() that deals with abstract file-like
    objects, instead of interacting with the filesystem.
    """
    write_kwargs = {}

    encoding, _ = std_tokenize.detect_encoding(f_in.readline)
    write_kwargs["encoding"] = encoding
    f_in.seek(0)

    tokens = unasync.tokenize(f_in)
    tokens = unasync.unasync_tokens(tokens)
    result = unasync.untokenize(tokens)

    f_out.write(result)
