import os
import time
import json
import asyncio
from kasa import SmartBulb, Discover
import pprint
pp = pprint.PrettyPrinter(indent=2)


from flask import Flask, abort, request


app = Flask(__name__)


ip = 0

devices = asyncio.run(Discover.discover())
for addr, dev in devices.items():
    asyncio.run(dev.update())
    ip = addr




@app.route("/")
async def turn_off():
    print("IP IS: ")
    print(ip)
    print("END IP")
    if(ip != 0):
        p = SmartBulb(ip)

        await p.update()
        # await p.turn_off()
        # await p.turn_on()

        await p.set_brightness(0, transition=3500)
        time.sleep(3.5)
        await p.turn_off()

        return(p.alias)


@app.route("/on")
async def turn_on():
    print(ip)
    if(ip != 0):
        p = SmartBulb(ip)

        await p.update()
        # await p.turn_off()
        await p.turn_on()
        await p.set_brightness(100, transition=2000)
        # await p.set_brightness(0, 2000)


        return(p.alias)


@app.route('/plex', methods=['POST'])
async def plex():
    print("wow")
    data = json.loads(request.form['payload'])

    # pp.pprint(data['Metadata'])
    print(data['event'])
    if(data['event'] == 'media.stop'):
        await turn_on()
    elif(data['event'] == 'media.pause'):
        await turn_on()
    elif(data['event'] == 'media.resume'):
        await turn_off()
    elif(data['event'] == 'media.play'):
        await turn_off()
    # print(data)
    return 'OK'
