def getSum(a, b):
    while b:
        a, b = (a ^ b), (a & b) << 1
    return a

# encoding function
def encoding(intText, b, it, bits):
  #kol kart 4, nes darom kad keiciam po du bitukus ir tada turim kiekvienai
  #raidei/char 4 poras.
  bReplaced = b & 255-(2**bits-1)
  if bits == 2 :
    if (it < len(intText)*4):
        m = it
        if (it >= len(intText)):
            m = it%len(intText)
        if (it < len(intText)):
          intText[m] = (intText[m] & 192)
          intText[m] = intText[m] >> 6
        elif (len(intText) <= it < len(intText)*2):
          intText[m] = (intText[m] & 48)
          intText[m] = intText[m] >> 4
        elif (len(intText)*2 <= it < len(intText)*3):
          intText[m] = (intText[m] & 12)
          intText[m] = intText[m] >> 2
        elif (len(intText)*3 <= it < len(intText)*4):
          intText[m] = (intText[m] & 3)
        b = getSum(bReplaced, intText[m])
        
  elif bits == 4:
    if (it < len(intText)*2):
      m = it
      if (it >= len(intText)):
        m = it%len(intText)
      if (it < len(intText)):
        intText[m] = (intText[m] & 240)
        intText[m] = intText[m] >> 4
      elif (len(intText) <= it < len(intText)*2):
        intText[m] = (intText[m] & 15)
      b = getSum(bReplaced, intText[m])
  elif bits == 6:
    if (it < len(intText)*2):
      m = it
      if (it >= len(intText)):
        m = it%len(intText)
      if (it < len(intText)):
        intText[m] = (intText[m] & 252)
        intText[m] = intText[m] >> 2
      elif (len(intText) <= it < len(intText)*2):
        intText[m] = (intText[m] & 3)
      b = getSum(bReplaced, intText[m])
  elif bits == 8:
    if (it < len(intText)*2):
      m = it
      if (it >= len(intText)):
        m = it%len(intText)
      b = getSum(bReplaced, intText[m])

  return(b)

# get two last bits       
def last2bits(hindex):
  return (hindex & 3)


def getRGBValue(rgbValue, img_resized):
  [r, g, b] = img_resized 
  if rgbValue == 'r':
    return r
  elif rgbValue == 'g':
    return g
  else:
    return b

def rshift(val, n): return (val % 0x100000000) >> n


# read like Hilbert curve 
def hilbert2xy(hindex, N, text, bits, it, img_resized, rgbValue):
  positions = [
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0]
  ]
  
  tmp = positions[last2bits(hindex)]
  hindex = rshift(hindex, 2)
  x = tmp[0]
  y = tmp[1]
  for n in range(4, N+1):
    if (n & (n-1) == 0) :    
      n2 = n/2
      if (last2bits(hindex) == 0):
        tmp = x
        x = y
        y = tmp
      elif (last2bits(hindex) == 1):
        x = x
        y = y + n2
      elif (last2bits(hindex) == 2):
        x = x + n2
        y = y + n2
      elif (last2bits(hindex) == 3):
        tmp = y
        y = (n2 - 1) - x
        x = (n2 - 1) - tmp
        x = x + n2

      hindex = rshift(hindex, 2)
  bb = getRGBValue(rgbValue, img_resized[x,y])   
  intText = [int(format(ord(x), '08b'), 2) for x in text]
  bb = encoding(intText, bb, it, bits)
  [r, g, b] = img_resized[x, y] 
  if (rgbValue == 'r'):
    r = bb
  elif (rgbValue == 'g'):
    g = bb
  else:
    b = bb
  img_resized[x,y] = r,g,b      
  return(x,y)
