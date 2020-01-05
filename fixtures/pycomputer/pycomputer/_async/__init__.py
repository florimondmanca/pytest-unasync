class AsyncComputer:
    async def compute(self, a: int, b: int) -> int:
        # Maybe do some unasync-able 'await' operations here...
        return a + b
