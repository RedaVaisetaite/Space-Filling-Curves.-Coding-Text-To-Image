
#decoding function
def decoding(shift, b, bits):
  if (bits == 2):
    bb = (b & 3)    
  elif (bits == 4):
    bb = (b & 15)
  elif (bits == 8):
    bb = b
  bb = bb << shift 
        
  # elif bits == 4:
  #   if (it < len(intText)*2):
  #     m = it
  #     if (it >= len(intText)):
  #       m = it%len(intText)
  #     if (it < len(intText)):
  #       intText[m] = (intText[m] & 240)
  #       intText[m] = intText[m] >> 4
  #     elif (len(intText) <= it < len(intText)*2):
  #       intText[m] = (intText[m] & 15)
  #     b = getSum(bReplaced, intText[m])
  # elif bits == 6:
  #   if (it < len(intText)*2):
  #     m = it
  #     if (it >= len(intText)):
  #       m = it%len(intText)
  #     if (it < len(intText)):
  #       intText[m] = (intText[m] & 252)
  #       intText[m] = intText[m] >> 2
  #     elif (len(intText) <= it < len(intText)*2):
  #       intText[m] = (intText[m] & 3)
  #     b = getSum(bReplaced, intText[m])
  # elif bits == 8:
  #   if (it < len(intText)*2):
  #     m = it
  #     if (it >= len(intText)):
  #       m = it%len(intText)
  #     b = getSum(bReplaced, intText[m])

  return(bb)

# gauti tik paskutinius du bitukus       
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


#nuskaityti kaip hilberto seka 
def hilbert2xy(hindex, N, shift, bits, img_resized, rgbValue):
  # !!!!!!!!!!!!!!!!!! it gal net nereikia !!!!!!!!!!!!!!!!!
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
  #print(x,y)
  color = getRGBValue(rgbValue, img_resized[x,y])   
  bb = decoding(shift, color, bits)
  return(bb)
    
