import aiohttp
import asyncio

import json

import falcon
from falcon import testing, media, http_status
from hio.base import doing

from dkr.core import resolving, webbing

from hio.base import tyming
from hio.core import http

from keri import help, kering
from keri.app import configing, habbing, oobiing
from keri.core import coring
from keri.db import basing
from keri.end import ending
from keri.help import helping

import os
import queue
import threading
import time
        
class PingResource:
   def on_get(self, req, resp):
      """Handles GET requests"""
      resp.status = falcon.HTTP_200
      resp.content_type = falcon.MEDIA_TEXT
      resp.text = (
         'Pong'
      )

def test_service():
    port = 7676
    
    with habbing.openHby(name="service") as hby:
        hab = hby.makeHab(name="service")
        aid = "ELCUOZXs-0xn3jOihm0AJ-L8XTFVT8SnIpmEDhFF9Kz_"
        did = f"did:web:127.0.0.1%3a{port}:{aid}"
        
        print("Current working dir", os.getcwd())
        cf = configing.Configer(name="config-test",
                        headDirPath="./volume/dkr/examples/my-scripts",
                        base="",
                        temp=False,
                        reopen=True,
                        clear=False)

        # Configure the did doc and keri cesr URL
        ddurl = f'http://127.0.0.1:{port}/{aid}/did.json'
        kcurl = f'http://127.0.0.1:{port}/{aid}/keri.cesr'
        purl = f"http://127.0.0.1:{port}/ping"
        puburl = "http://example.org"

        app = falcon.App(middleware=falcon.CORSMiddleware(
        allow_origins='*', allow_credentials='*',
        expose_headers=['cesr-attachment', 'cesr-date', 'content-type', 'signature', 'signature-input',
                        'signify-resource', 'signify-timestamp']))

        print("CORS  enabled")
        app.add_middleware(middleware=HandleCORS())
        app.req_options.media_handlers.update(media.Handlers())
        app.resp_options.media_handlers.update(media.Handlers())
        # falcon.App instances are callable WSGI apps

        app.add_route('/ping', PingResource())
        webbing.setup(app, hby, cf)
        # app.add_route('/{aid}/did.json', DidWebsEnd())
        # app.add_route('/{aid}/keri.cesr', KeriCesrEnd(aid=aid))

        server = http.Server(host="127.0.0.1",port=port, app=app, scheme="http")
        httpServerDoer = http.ServerDoer(server=server)

        # client = testing.TestClient(app=app)        
        # rep = client.simulate_get('/example')
        # assert rep.status == falcon.HTTP_OK
        # assert rep.text == '\nHello World\n\n'

        limit = 2.0
        tock = 0.03125
        doers = [httpServerDoer]
        doist = doing.Doist(limit=limit, tock=tock, doers=doers)
        # doist.do(doers=doers)

        doist.enter()
        tymer = tyming.Tymer(tymth=doist.tymen(), duration=doist.limit)

        pstat = None
        ptres = queue.Queue()
        pt = threading.Thread(target=resolving.loadUrl, args=(purl,ptres))
        pt.start()
        
        ddstat = None
        ddtres = queue.Queue()
        ddt = threading.Thread(target=resolving.loadUrl, args=(ddurl,ddtres))
        ddt.start()
        
        kcstat = None
        kctres = queue.Queue()
        kct = threading.Thread(target=resolving.loadUrl, args=(kcurl,kctres))
        kct.start()
        
        while pstat == None or ddtres == None or kctres == None:
            # resp = resDoer.loadUrl(ddurl)
            # status = asyncio.run(call(eurl))
            # resDoer.loadUrl(kcurl)
            # resDoer.resolve(tymth=doist.tymen(), tock=doist.tock)
            time.sleep(2)
            doist.recur()

            resp = ptres.get()
            pstat = resp.status_code
            assert pstat == 200
            print("Got ping response content", resp.content)
            
            resp = ddtres.get()
            ddstat = resp.status_code
            assert ddstat == 200
            print("Got dd response content", resp.content)
            
            resp = kctres.get()
            kcstat = resp.status_code
            assert kcstat == 200
            print("Got kc response content", resp.content)
        doist.exit()

        

        """Done Test"""
    
class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise http_status.HTTPStatus(falcon.HTTP_200, text='\n')