import inspect
import io
import textwrap
import types
import typing

import pytest

from .unasync_extras import unasync_fileobj
from .utils import get_logger

logger = get_logger(__name__)


def pytest_configure(config: typing.Any) -> None:
    """Inject documentation."""
    config.addinivalue_line(
        "markers", "unasync: mark the test to be processed by unasync",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> typing.Iterator[None]:
    if "unasync" in pyfuncitem.keywords:
        pyfuncitem.obj = unasync_function(pyfuncitem.obj)
    yield


def unasync_function(async_func: types.FunctionType) -> types.FunctionType:
    assert inspect.iscoroutinefunction(async_func)

    sync_func_name = async_func.__name__ + "_sync"

    async_source = inspect.getsource(async_func)
    sync_source = _unasync_source_code(async_source)
    # This could be rewritten if/when unasync supports
    # custom 'ASYNC_TO_SYNC' translations.
    sync_source = sync_source.replace(
        f"def {async_func.__name__}(", f"def {sync_func_name}("
    )

    # NOTE: we must make sure imports available to 'async_func' are available
    # to the generated sync func too.
    namespace = async_func.__globals__.copy()
    exec(sync_source, namespace)
    sync_func = namespace[sync_func_name]

    assert inspect.isfunction(sync_func)
    assert not inspect.iscoroutinefunction(sync_func)

    logger.debug(
        "Transformed function '%s' into:\n\n%s\n",
        async_func.__name__,
        textwrap.indent(sync_source, 4 * " "),
    )

    return sync_func


def _unasync_source_code(source: str) -> str:
    output = io.StringIO()
    unasync_fileobj(f_in=io.BytesIO(source.encode("utf-8")), f_out=output)
    return output.getvalue()[:-1]
