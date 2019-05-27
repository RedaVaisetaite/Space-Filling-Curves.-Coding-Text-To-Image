def decoding(b, it, bits, textLength):
  if (bits == 2):
    bb = (b & 3)
    if (it < textLength*4):
        if (it < textLength):        
          bb = bb << 6
        elif (textLength <= it < textLength*2):
          bb = bb << 4
        elif (textLength*2 <= it < textLength*3):
          bb = bb << 2
        elif (textLength*3 <= it < textLength*4):
          bb = bb
  elif (bits == 4):
    bb = (b & 15)
    if (it < textLength*2):
      if (it < textLength):
        bb = bb << 4
      elif (textLength <= it < textLength*2):
        bb = bb
  elif (bits == 6):    
    if (it < textLength*2):
      if (it < textLength):
        bb = (b & 63) 
        bb = bb << 2
      elif (textLength <= it < textLength*2):
        bb = (b & 3)
  elif (bits == 8):
    if (it < textLength*2):
      bb = b
  return(bb)


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

def hilbert2xy(hindex, N, textLength, bits, it, img_resized, rgbValue):
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
  letter = decoding(bb, it, bits, textLength)
  return (letter) 
