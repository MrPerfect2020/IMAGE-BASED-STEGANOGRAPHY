
import PIL.Image
# aes encription 
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from tkinter import *
from tkinter import ttk


__key__ = hashlib.sha256(b'123456789012345678').digest()

def encrypt(raw):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key= __key__, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(__key__, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))

def genData(data):

		newd = []
		data = encrypt(data)
		
		for i in str(data):
			
			newd.append(format(ord(str(i)), '08b'))
		return newd

def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode(data,img_file):
	# img = input("Enter image name(with extension) : ")
	
	image = PIL.Image.open(img_file, 'r')

	# data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = "output.png"
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode(img):
	#img = input("Enter image name(with extension) : ")
	image = PIL.Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())
	
	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		
		if (pixels[-1] % 2 != 0):
			data = str(data).replace("b'",'').replace("'",'')
			return decrypt(data)
			

# Main Function
def main():
    #Create an instance of Tkinter frame
	win= Tk()

	#Set the geometry of Tkinter frame
	win.geometry("750x450")
	global entry 
	global entry2
	def display_text(val):
		string= entry.get()
		string2 = entry2.get()
		
		if val == "encrypt":
			encode(string,string2)
			label.configure(text="File saved output.png", font=("Courier 15 bold"))
		else:
			decoded_value = "Decrpted Text: "
			decoded_value += decode(string2)
			label.configure(text=decoded_value, font=("Courier 15 bold"))
		


	#Initialize a Label to display the User Input
	Label(win, text="Welcome ",width=20, font=("Courier 22 bold")).place(x=200, y=20)
	#Create an Entry widget to accept User Input
	label1 = Label(win, text="     Input Text :",width=20, font=("Courier 10 bold"))
	label1.place(x=70, y=90)
	entry= Entry(win,width= 40)
	entry.focus_set()
	entry.place(x=200, y=90)

	# image path 
	lable2 = Label(win,text="Past image Path :",width=20,font=("Courier 10 bold"))
	lable2.place(x=70, y=150)
	entry2= Entry(win,width= 40)
	entry2.place(x=200, y=150)
	#Create a Button to validate Entry Widget
	ttk.Button(win, text= "Encryt",width= 10, command= lambda val = "encrypt" :display_text(val) ,padding=10).place(x=200, y=220)
	ttk.Button(win, text= "Decryt",width= 10, command= lambda val = "decrypt" :display_text(val),padding=10).place(x=400, y=220)
	label=Label(win, text="", font=("Courier 9 bold"))
	label.place(x=200, y=320)
	lablel3 =Label(win, text="", font=("Courier 9 bold"))
	lablel3.place(x=250, y=300)
	win.mainloop()
	# a = int(input(":: Welcome to Steganography ::\n"
	# 					"1. Encode\n2. Decode\n"))
	# if (a == 1):
	# 	encode()

	# elif (a == 2):
	# 	print("Decoded Word : " + decode())
	# else:
	# 	raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :

	# Calling main function
	main()
