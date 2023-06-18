# [![Goblin logo](https://git.qoto.org/goblin-ogm/goblin/uploads/bb8f7349fdb9aa2a7a244e4c95b380a7/goblin-logo.png)  AIO Gremlin](http://goblin-ogm.com) - Now known as [gremlinpy](https://github.com/jerlendds/gremlinpy) - Patched by [jerlendds](https://github.com/jerlendds)

[![tests](http://git.qoto.org/goblin-ogm/gremlinpy/badges/master/pipeline.svg)](http://git.qoto.org/goblin-ogm/gremlinpy/commits/master)
[![Requirements](https://requires.io/github/goblin-ogm/gremlinpy/requirements.svg?branch=master)](https://requires.io/github/goblin-ogm/gremlinpy/requirements/?branch=master)
[![test coverage](http://git.qoto.org/goblin-ogm/gremlinpy/badges/master/coverage.svg)](http://git.qoto.org/goblin-ogm/gremlinpy/commits/master)
[![codecov](https://codecov.io/gh/goblin-ogm/gremlinpy/branch/master/graph/badge.svg)](https://codecov.io/gh/goblin-ogm/gremlinpy)
[![Codacy](https://api.codacy.com/project/badge/Grade/99c4b7d53ee94c85b95433ee4ff6230c)](https://www.codacy.com/gh/goblin-ogm/gremlinpy)
[![Scrutinizer](https://img.shields.io/scrutinizer/quality/g/goblin-ogm/gremlinpy/master.svg?style=flat)](https://scrutinizer-ci.com/g/goblin-ogm/gremlinpy)

[![PyPi](https://img.shields.io/pypi/v/gremlinpy.svg?style=flat)](https://pypi.python.org/pypi/gremlinpy)
[![Supported Versions](https://img.shields.io/pypi/pyversions/gremlinpy.svg?style=flat)](https://pypi.python.org/pypi/gremlinpy)
[![Downloads](https://img.shields.io/pypi/dm/gremlinpy.svg?style=flat)](https://pypi.python.org/pypi/gremlinpy)
[![SemVer](https://img.shields.io/badge/SemVer-v2.0.0-green)](https://semver.org/spec/v2.0.0.html)
[![docs](https://readthedocs.org/projects/gremlinpy/badge/?version=latest)](https://gremlinpy.readthedocs.io/en/latest/)
[![Gitter](https://badges.gitter.im/goblin-ogm/gremlinpy.svg)](https://gitter.im/goblin-ogm/gremlinpy)


*Installation:*

```py
pip install git+https://github.com/jerlendds/gremlinpy.git
```

*Message from jerlendds*

1. I changed the package name to `gremlinpy` so my imports are slightly shorter

2. I was trying to use the `gremlin-python`, `goblin`, `aiogremlin` in [my FastAPI app](https://github.com/jerlendds/osintbuddy) but I kept running into a loop error from the `aiogremlin` library. This patch fixes that and later on I may publish it to PyPi after I get some use out of this fix.

*Example usage from my [OSINTBuddy](https://github.com/jerlendds/osintbuddy) app*

```py
from gremlinpy import DriverRemoteConnection, Graph
from gremlinpy.process.graph_traversal import AsyncGraphTraversal
from gremlin_python.process.traversal import T, Cardinality

def process_vertices(graph: List[dict]):
    output = []
    for obj in v:
        out = {
            "id":  obj[T.id],
            "label": obj[T.label],
        }
        del obj[T.id]
        del obj[T.label]
        for k, v in obj.items():
            out[k] = v[0]
        output.append(out)
    return output

async def some_async_function(plugin_label):
    async with await DriverRemoteConnection.open('ws://janus:8182/g', 'g') as connection:
        g: AsyncGraphTraversal = Graph().traversal().withRemote(connection)
        await g.addV('Some Label').property('id', 1). \
            property(Cardinality.single, 'name', 'Apache'). \
            property('lastname', 'WTF'). \
            next()
        vertices = await g.V().valueMap(True).toList()
        json_graph: List[dict] = process_vertices(vertices)
        print(json_graph)

```


An asynchronous DSL for the Gremlin-Python driver

**Licensed under the Apache Software License v2**

`gremlinpy` is an asynchronous DSL based on the official `Gremlin-Python` GLV designed for integration with
event loop based asynchronous Python networking libraries, including `asyncio`,
`aiohttp`, and `tornado`. It uses the `async/await` syntax introduced
in PEP 492, and is therefore Python 3.5+ only.

`gremlinpy` tries to follow `Gremlin-Python` as closely as possible both in terms
of API and implementation. It is released according to the TinkerPop release schedule.

`gremlinpy` is built directly on top of TinkerPop and allows access to all of the internals. This ensures all the
TinkerPop features are available to the end-user. The TinkerPop stack provides several tools which can be used to work
with `gremlinpy`.

* **Gremlin**, a database agnostic query language for Graph Databases.
* **Gremlin Server**, a server that provides an interface for executing Gremlin on remote machines.
* a data-flow framework for splitting, merging, filtering, and transforming of data
* **Graph Computer**, a framework for running algorithms against a Graph Database.
* Support for both **OLTP** and **OLAP** engines.
* **TinkerGraph** a Graph Database and the reference implementation for TinkerPop.
* Native **Gephi** integration for visualizing graphs.
* Interfaces for most major Graph Compute Engines including **Hadoop M/R**. **Spark**, and **Giraph**.

`gremlinpy` also supports any of the many databases compatible with TinkerPop including the following.

 * [JanusGraph](http://janusgraph.org/)
 * [Titan](http://thinkaurelius.github.io/titan/)
 * [Neo4j](http://neo4j.com)
 * [OrientDB](http://www.orientechnologies.com/orientdb/)
 * [MongoDB](http://www.mongodb.org)
 * [Oracle NoSQL](http://www.oracle.com/us/products/database/nosql/overview/index.html)
 * TinkerGraph

 Some unique feature provided by the Goblin OGM include:

* High level asynchronous *Object Graph Mapper* (OGM) - provided by [goblin](https://git.qoto.org/goblin-ogm/goblin)
* Integration with the *official gremlin-python Gremlin Language Variant* (GLV)
* Native Python support for asynchronous programing including *coroutines*, *iterators*, and *context managers* as specified in [PEP 492](https://www.python.org/dev/peps/pep-0492/)
* *Asynchronous Python driver* for the Gremlin Server
* Async `Graph` implementation that produces *native Python GLV traversals*

## Getting Started

```python
import asyncio
from gremlinpy import DriverRemoteConnection, Graph


loop = asyncio.get_event_loop()


async def go(loop):
  remote_connection = await DriverRemoteConnection.open(
    'ws://localhost:8182/gremlin', 'g')
  g = Graph().traversal().withRemote(remote_connection)
  vertices = await g.V().toList()
  await remote_connection.close()
  return vertices


vertices = loop.run_until_complete(go(loop))
print(vertices)
# [v[1], v[2], v[3], v[4], v[5], v[6]]
```
## Donating

[![Librepay](http://img.shields.io/liberapay/receives/goblin-ogm.svg?logo=liberapay)](https://liberapay.com/goblin-ogm/donate)

As an open-source project we run entierly off donations. Buy one of our hardworking developers a beer by donating with one of the above buttons. All donations go to our bounty fund and allow us to place bounties on important bugs and enhancements.

## Support and Documentation

The official homepage for the project is at [http://goblin-ogm.com](http://goblin-ogm.com). The source is officially hosted on [QOTO GitLab here](https://git.qoto.org/goblin-ogm/gremlinpy) however an up-to-date mirror is also maintained on [Github here](https://github.com/goblin-ogm/gremlinpy).

Documentation: [latest](http://goblin-ogm.qoto.io/gremlinpy)

For support please use [Gitter](https://gitter.im/goblin-ogm/gremlinpy) or the [official Goblin mailing list and Discourse forum](https://discourse.qoto.org/c/PROJ/GOB).

Please file bugs and feature requests on [QOTO GitLab](https://git.qoto.org/goblin-ogm/gremlinpy/issues) our old archived issues can still be viewed on [Github](https://github.com/davebshow/gremlinpy/issues) as well.

Aparapi conforms to the [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html) standard. That means the version of a release isnt arbitrary but rather describes how the library interfaces have changed. Read more about it at the [Semantic Versioning page](http://semver.org/spec/v2.0.0.html).

## Related Projects

This particular repository only represents the one component in a suite of libraries. There are several other related repositories worth taking a look at.

* [Goblin](https://git.qoto.org/goblin-ogm/goblin) - The main library, the Goblin OGM
* [Goblin Buildchain](https://git.qoto.org/goblin-ogm/goblin-buildchain) - Docker image containing all the needed tools to build and test Goblin.
* [Python Gremlin Server](https://git.qoto.org/goblin-ogm/gremlin-server-python) - Vanilla Gremlin-server with Python Script Engine loaded, used for integration testing.
