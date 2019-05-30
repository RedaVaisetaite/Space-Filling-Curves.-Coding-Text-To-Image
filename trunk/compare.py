import matplotlib.pyplot as plt
from PIL import Image

original = "kodavimui/v13-72rez.png"
image1 = Image.open(original)
count0 = 0
count1 = 0
img1 = image1.load()
width, height = image1.size
for x in range(width):
    for y in range(height):
        r,g,b = image1.getpixel((x,y))
        c1 = r ^ 85
        c2 = g ^ 85
        c3 = b ^ 85
        count0 = count0 + bin(c1).count('0') + bin(c2).count('0') + bin(c3).count('0') 
        count1 = count1 + bin(c1).count('1') + bin(c2).count('1') + bin(c3).count('1')
print('count0: ', count0)
print('count1: ', count1)

coded = "uzkoduoti/analizei/rg_2_12448txt.png"
# coded = "uzkoduoti/analizei/rg_2_20034png.png"
# coded = "uzkoduoti/analizei/rg_2_3023input.png"
image2 = Image.open(coded)
count0_2 = 0
count1_2 = 0
img1 = image2.load()
width, height = image2.size
for x in range(width):
    for y in range(height):
        r,g,b = image2.getpixel((x,y))
        c1 = r ^ 85
        c2 = g ^ 85
        c3 = b ^ 85
        count0_2 = count0_2 + bin(c1).count('0') + bin(c2).count('0') + bin(c3).count('0') 
        count1_2 = count1_2 + bin(c1).count('1') + bin(c2).count('1') + bin(c3).count('1')
print('Užkoduotas paveiksliukas')
print('count0: ', count0_2)
print('count1: ', count1_2)

proc1 = float(count0 / (count0+count1) * 100)
proc2 = float(count0_2 / (count0_2+count1_2) * 100)
proc = [proc1, proc2]
fig = plt.figure("Images")
images = ("Originalus", image1), ("Užkoduotas", image2)
 
# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 2, i + 1)
	ax.set_title(name + "\n\nSutapimas su baltu triukšmu procentais: %.2f" % (proc[i]))
	# ax.set_xlabel("\nSutapimas su baltu triukšmu procentais: %.2f" % (proc[i]))
	# ax.suptitle("Sutapimo procentas: %.2f" % (proc[i]))
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
 
# show the figure
plt.show()
