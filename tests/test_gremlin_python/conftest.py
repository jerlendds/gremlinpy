'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''
'''THIS FILE HAS BEEN MODIFIED BY DAVID M. BROWN TO SUPPORT PEP 492'''
import pytest

from aiogremlin.structure.graph import Graph
from aiogremlin.remote.driver_remote_connection import DriverRemoteConnection
from aiogremlin.driver.protocol import GremlinServerWSProtocol
from aiogremlin.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.driver.serializer import GraphSONMessageSerializer
from gremlin_python.process.traversal import T


@pytest.fixture
def client(event_loop, cluster):
    try:
        client = event_loop.run_until_complete(cluster.connect())
    except OSError:
        pytest.skip('Gremlin Server is not running')
    else:
        return client

@pytest.fixture
def remote_connection(event_loop, gremlin_url):
    try:
        remote_conn = event_loop.run_until_complete(
            DriverRemoteConnection.open(gremlin_url, 'g'))
    except OSError:
        pytest.skip('Gremlin Server is not running')
    else:
        return remote_conn

@pytest.fixture(autouse=True)
def run_around_tests(remote_connection, event_loop):
    g = Graph().traversal().withRemote(remote_connection)

    async def create_graph():
        await g.V().drop().iterate()
        software1 = await g.addV("software").property("name", "lop").property("lang", "java").property(T.id, 3).next()
        software2 = await g.addV("software").property("name", "ripple").property("lang", "java").property(T.id, 5).next()
        person1 = await g.addV("person").property("name", "marko").property("age", "29").property(T.id, 1).next()
        person2 = await g.addV("person").property("name", "vadas").property("age", "27").property(T.id, 2).next()
        person3 = await g.addV("person").property("name", "josh").property("age", "32").property(T.id, 4).next()
        person4 = await g.addV("person").property("name", "peter").property("age", "35").property(T.id, 6).next()

        knows1 = await g.addE("knows").from_(person1).to(person2).property("weight", 0.5).property(T.id, 7).next()
        knows2 = await g.addE("knows").from_(person1).to(person3).property("weight", 1,0).property(T.id, 8).next()
        created1 = await g.addE("created").from_(person1).to(software1).property("weight", 0.4).property(T.id, 9).next()
        created2 = await g.addE("created").from_(person3).to(software2).property("weight", 1.0).property(T.id, 10).next()
        created3 = await g.addE("created").from_(person3).to(software1).property("weight", 1.0).property(T.id, 11).next()
        created4 = await g.addE("created").from_(person4).to(software1).property("weight", 0.2).property(T.id, 12).next()

    event_loop.run_until_complete(create_graph())

    yield
