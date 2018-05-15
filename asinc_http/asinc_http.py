from aiohttp import web
import asyncio
import os
import aiohttp


directory="E:\\python_h\\asinc0_http\\tmp"

import sys

class Task():
    def __init__(self,file,loop):
        self._loop=loop
        self._app = web.Application()
        self.parametres(file)
        self.create()


    def create(self):
        self._app.add_routes([web.get('/{name}', self.answer), web.get('/find/{name}', self.answer_server)])
        handler = self._app._make_handler()
        coroutine = self._loop.create_server(handler, '0.0.0.0', self._port)
        server = self._loop.run_until_complete(coroutine)
        address, port = server.sockets[0].getsockname()
        print('App started on http://{}:{}'.format(address, port))


    def parametres(self,file):
        data = open(os.path.join(directory,file), 'r')
        lines=[]
        for line in data:
            lines.append(line.strip('\n'))
        self._directory =lines[0]
        self._port =lines[1]
        self._save=lines[2]
        self._servers=[]
        for i in range(3,len(lines)):
            self._servers.append(lines[i])
        data.close()

    def ret_app(self):
        return self._app

    async def fetch(self,session, url):
        async with session.get(url) as response:
            return await response.text()

    async def mains(self,i,n):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, f'http://localhost:{i}/find/{n}')
            self.text=html

    async def answer_server(self, request):
        name = request.match_info.get('name')
        if os.path.isfile(os.path.join(self._directory, name)):
            data = open(os.path.join(self._directory, name), 'r')
            text = f'{data.read()}'
            data.close()
        else:
            text = 'error'
        return web.Response(text=text)

    def save_file(self,name,value):
        data = open(os.path.join(self._directory, name), 'w')
        data.write(value)
        data.close()

    async def answer(self,request):
        name = request.match_info.get('name')
        if os.path.isfile(os.path.join(self._directory, name)):
            data = open(os.path.join(self._directory, name), 'r')
            self.text = f'{data.read()}'
            data.close()
            return web.Response(text=self.text)
        else:
            for port in self._servers:
                n=await asyncio.ensure_future(self.mains(port,name))
                if self.text !='error':
                    if self._save=='yes':
                        self.save_file(name,self.text)
                    return web.Response(text=self.text)
                else:
                    continue
            if self.text =='error':
                return web.Response(text='error 404')



def start(files):
    try:
        loop = asyncio.get_event_loop()

        for file in files:
            Task(file,loop)

        loop.run_forever()

        loop.close()
    except Exception as e:
        sys.stderr.write('Error: ' + format(str(e)) + "\n")
        sys.exit(1)


file=['a.yaml','b.yaml','c.yaml']
start(file)

