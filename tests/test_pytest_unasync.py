import typing


def test_package(testdir: typing.Any) -> None:
    testdir.makeconftest(
        """
        import pytest

        @pytest.fixture(
            params=[
                pytest.param("sync", marks=pytest.mark.unasync),
                pytest.param("asyncio", marks=pytest.mark.asyncio),
            ],
        )
        def concurrency_environment(request):
            return request.param
        """
    )

    testdir.makepyfile(
        """
        import pytest

        import pycomputer


        @pytest.mark.usefixtures("concurrency_environment")
        async def test_compute() -> None:
            computer = pycomputer.AsyncComputer()
            assert await computer.compute(1, 2) == 3


        @pytest.mark.unasync
        async def test_hello():
            async def hello():
                return "Hello, world"

            assert await hello() == "Hello, world"
        """
    )

    result = testdir.runpytest("-s")
    result.assert_outcomes(passed=3)
