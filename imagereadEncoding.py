def getSum(a, b):
    while b:
        a, b = (a ^ b), (a & b) << 1
    return a

# (2) Get image width & height in pixels
#[xs, ys] = img.size    

#check if the color is not out of limit
#def clamp(x): 
#  return max(0, min(x, 255))

#encoding function
def encoding(intText, b, it, bits):
  #kol kart 4, nes darom kad keiciam po du bitukus ir tada turim kiekvienai
  #raidei/char 4 poras.
  if (it < len(intText)*4):
      m = it
      if (it >= len(intText)):
          m = it%len(intText)
      #dabar darau tik su dviejais bitais. bet jei reiktu su n bitu, tai
      #tada darytume taip:
      #and'int su 2**n-1 raides bitais ir 255-2**n-1 su spalvos bitais
      bReplaced = b & 255-(2**bits-1)
      if (it < len(intText)):
        intText[m] = (intText[m] & 192)
        intText[m] = intText[m] >> 6
        
            #print(intText[letter])
      elif (len(intText) <= it < len(intText)*2):
        intText[m] = (intText[m] & 48)
        intText[m] = intText[m] >> 4
            #print(bin(letter))
            #print(bin(48))
      elif (len(intText)*2 <= it < len(intText)*3):
        intText[m] = (intText[m] & 12)
        intText[m] = intText[m] >> 2
            #print(bin(letter))
      elif (len(intText)*3 <= it < len(intText)*4):
        intText[m] = (intText[m] & 3)
      
      b = getSum(bReplaced, intText[m])
  return(b)

#nuskaityti kaip hilberto seka        
def last2bits(hindex):
  return (hindex & 3)

def rshift(val, n): return (val % 0x100000000) >> n

def hilbert2xy(hindex, N, text, bits, it, img_resized):
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
  [r, g, b] = img_resized[x, y]
  intText = [int(format(ord(x), '08b'), 2) for x in text]
  b = encoding(intText, b, it, bits)
  img_resized[x,y] = r,g,b
      
  return(x,y)
