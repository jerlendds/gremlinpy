from aiogremlin.process.traversal import AsyncTraversalStrategies
from aiogremlin.remote.remote_connection import AsyncRemoteStrategy

from gremlin_python.process import graph_traversal, traversal


class AsyncGraphTraversal(graph_traversal.GraphTraversal):
    """Implements async iteration protocol and updates relevant methods"""

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.traversers is None:
            await self.traversal_strategies.apply_strategies(self)
        if self.last_traverser is None:
            self.last_traverser = await self.traversers.__anext__()
        object = self.last_traverser.object
        self.last_traverser.bulk = self.last_traverser.bulk - 1
        if self.last_traverser.bulk <= 0:
            self.last_traverser = None
        return object

    async def toList(self):
        """Reture results as ``list``."""
        results = []
        async for result in self:
            results.append(result)
        return results

    async def toSet(self):
        """Return results as ``set``."""
        results = set()
        async for result in self:
            results.add(result)
        return results

    async def iterate(self):
        """Iterate over results."""
        while True:
            try:
                await self.nextTraverser()
            except StopAsyncIteration:
                return self

    async def nextTraverser(self):
        """Return next traverser."""
        if self.traversers is None:
            await self.traversal_strategies.apply_strategies(self)
        if self.last_traverser is None:
            return await self.traversers.__anext__()
        else:
            temp = self.last_traverser
            self.last_traverser = None
            return temp

    async def next(self, amount=None):
        """Return iterator with optionaly defined amount of items."""
        if not amount:
            try:
                return await self.__anext__()
            except StopAsyncIteration:
                return
        results = []
        for i in range(amount):
            try:
                result = await self.__anext__()
            except StopAsyncIteration:
                return results
            results.append(result)
        return results


class __(graph_traversal.__):

    graph_traversal = AsyncGraphTraversal


class AsyncGraphTraversalSource(graph_traversal.GraphTraversalSource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_traversal = AsyncGraphTraversal

    def withRemote(self, remote_connection):
        source = self.get_graph_traversal_source()
        source.traversal_strategies.add_strategies([AsyncRemoteStrategy(remote_connection)])
        return source

    def get_graph_traversal_source(self):
        return self.__class__(
            self.graph, AsyncTraversalStrategies(self.traversal_strategies),
            traversal.Bytecode(self.bytecode))
