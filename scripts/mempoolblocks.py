#! /usr/bin/python3
from datetime import datetime
from PIL import Image, ImageDraw, ImageColor
import json
import locale
import math
import subprocess
import time
import vicarioustext

urlmempool="https://mempool.space/api/v1/fees/mempool-blocks"
urlfeerecs="https://mempool.space/api/v1/fees/recommended"
# If you are running your own Mempool.space service, e.g., on MyNodeBTC, then uncomment the following
#urlmempool="http://127.0.0.1:4080/api/v1/fees/mempool-blocks"
#urlfeerecs="http://127.0.0.1:4080/api/v1/fees/recommended"

outputFile="/home/bitcoin/images/mempoolblocks.png"
color202020=ImageColor.getrgb("#202020")
color404040=ImageColor.getrgb("#404040")
color606060=ImageColor.getrgb("#606060")
color40C040=ImageColor.getrgb("#40C040")
color40FF40=ImageColor.getrgb("#40FF40")
color000000=ImageColor.getrgb("#000000")
colorFFFFFF=ImageColor.getrgb("#ffffff")

def drawsatssquare(draw,dc,dr,spf,satw,bpx,bpy):
    satsleft = spf
    for y in range(10):
        for x in range(10):
            if satsleft > 0:
                tlx = (bpx + (dc*11*satw) + (x*satw))
                tly = (bpy + (dr*11*satw) + (y*satw))
                brx = tlx+satw-2
                bry = tly+satw-2
                draw.rectangle(xy=((tlx,tly),(brx,bry)),fill=color40FF40)
            satsleft = satsleft - 1

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def drawmempoolblock(draw,x,y,w,h,blockinfo,mpb):
    blocksize=blockinfo["blockSize"]
    blockvsize=blockinfo["blockVSize"]
    transactions=blockinfo["nTx"]
    feeranges=list(blockinfo["feeRange"])
    feelow=feeranges[0]
    feehigh=feeranges[len(feeranges)-1]
    feemedian=blockinfo["medianFee"]
    depth=int(math.floor(w*.14))
    pad=2
    blockcolor=color40C040
    draw.polygon(xy=((x+pad,y+pad),(x+pad,y+h-pad-depth),(x+pad+depth,y+h-pad),(x+pad+depth,y+pad+depth)),outline=color202020,fill=color404040)
    draw.polygon(xy=((x+pad,y+pad),(x+pad+depth,y+pad+depth),(x+w-pad,y+pad+depth),(x+w-pad-depth,y+pad)),outline=color202020,fill=color606060)
    draw.polygon(xy=((x+pad+depth,y+pad+depth),(x+w-pad,y+pad+depth),(x+w-pad,y+h-pad),(x+pad+depth,y+h-pad)),outline=color202020,fill=blockcolor)
    centerx=x+depth+(int(math.floor((w-depth)/2)))
    descriptor="~" + str(int(math.floor(float(feemedian)))) + " sat/vB"
    vicarioustext.drawcenteredtext(draw, descriptor, 14, centerx, y+pad+(depth*2))
    descriptor=str(int(math.floor(float(feelow)))) + " - " + str(int(math.floor(float(feehigh)))) + " sat/vB"
    vicarioustext.drawcenteredtext(draw, descriptor, 14, centerx, y+pad+(depth*3))
    descriptor=convert_size(int(blocksize))
    vicarioustext.drawcenteredtext(draw, descriptor, 18, centerx, y+pad+(depth*4))
    locale.setlocale(locale.LC_ALL, '')
    descriptor='{:n}'.format(int(transactions)) + " transactions"
    vicarioustext.drawcenteredtext(draw, descriptor, 14, centerx, y+pad+(depth*5))
    descriptor="In ~" + str((mpb+1)*10) + " minutes"
    vicarioustext.drawcenteredtext(draw, descriptor, 14, centerx, y+pad+(depth*6))

def createimage(width=480, height=320):
    mempoolblocks = getmempoolblocks()
    feefastest, feehalfhour, feehour, feeminimum = getrecommendedfees()
    bw = width/3
    padtop=40
    im = Image.new(mode="RGB", size=(width, height))
    draw = ImageDraw.Draw(im)
    mpblist=list(mempoolblocks)
    mpblen=len(mpblist)
    for mpb in range(mpblen):
        if mpb > 2:
            break
        drawmempoolblock(draw,(width-((mpb+1)*bw)),padtop,bw,bw,mpblist[mpb],mpb)
    vicarioustext.drawcenteredtext(draw, "Mempool Block Fee Estimates", 24, int(width/2), int(padtop/2), colorFFFFFF, True)
    vicarioustext.drawcenteredtext(draw, "Next: " + str(feefastest), 20, int(width/8*1), height-padtop)
    vicarioustext.drawcenteredtext(draw, "30 Min: " + str(feehalfhour), 20, int(width/8*3), height-padtop)
    vicarioustext.drawcenteredtext(draw, "1 Hr: " + str(feehour), 20, int(width/8*5), height-padtop)
    vicarioustext.drawcenteredtext(draw, "Minimum: " + str(feeminimum), 20, int(width/8*7), height-padtop)
    vicarioustext.drawbottomrighttext(draw, "as of " + vicarioustext.getdateandtime(), 12, width, height)
    im.save(outputFile)

def getmempoolblocks():
    cmd = "curl --silent " + urlmempool
    try:
        cmdoutput = subprocess.check_output(cmd, shell=True).decode("utf-8")
        j = json.loads(cmdoutput)
        return j
    except subprocess.CalledProcessError as e:
        cmdoutput = "[]"
        j = json.loads(cmdoutput)
        return j

def getrecommendedfees():
    cmd = "curl --silent " + urlfeerecs
    try:
        cmdoutput = subprocess.check_output(cmd, shell=True).decode("utf-8")
        j = json.loads(cmdoutput)
        return j["fastestFee"], j["halfHourFee"], j["hourFee"], j["minimumFee"]
    except subprocess.CalledProcessError as e:
        return 1, 1, 1, 1

while True:
    createimage()
    time.sleep(300)
