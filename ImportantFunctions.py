directory=""

import os
import cv2
import imutils
import PIL
from PIL import Image
from PIL import ImageTk
import shutil
import re
import numpy as np
import csv
import tkinter as tk

def WriteWithNewLine(Categories, f):
    for categories in Categories:
        if categories == Categories[0]:
            f.write(categories) 
        else:
            f.write("\n" + categories)
            
#TEXT_FILE------------------------------------------------------------------------
def Read_Text_File(file_name):
    AllIn = []
    f = open(directory + file_name, "r+")
    AllIn.append(list(s.rstrip() for s in (f.readlines())))
    return

def Replace_Line(file_name, line_num, text):
    lines = open(directory + file_name, 'r').readlines()
    lines[line_num] = text + "\n"
    out = open(directory + file_name, 'w')
    out.writelines(lines)
    out.close()
    
#CSV_FILE------------------------------------------------------------------------
def GetInfoFromCSV(CSV_File, VariableName):
    CSV_File = directory + CSV_File
    with open(CSV_File) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='=')
        line_count = 0
        for row in csv_reader:
            if row[0] == VariableName:
                return row[1]

def ReplaceInfoToCSV2(CSV_File, VariableName, Value):
    CSV_File = directory + CSV_File
    with open(CSV_File) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='=')
        RowList = []
        for row in csv_reader:
            RowList.append(row)

    with open(CSV_File, mode='w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='=', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in RowList:
            if row[0] != VariableName:
                csv_writer.writerow(row)
            else:
                csv_writer.writerow([row[0],Value])

def tkGetEntryValue(Entry):
    v = tk.StringVar()
    Entry.configure(textvariable=v)
    return v.get()
#DATABASE-------------------------------------------------------------------------
def Create_DB(Database, *Categories):
    if (os.path.exists(directory + "Database/" + Database)==False):
        os.mkdir(directory + "Database/" + Database)
        os.mkdir(directory + "Database/" + Database + "/0000")
        f = open(directory + "Database/" + Database + "/0000/0000.txt", "w+")
        f.write("0\n")
        WriteWithNewLine(Categories, f)

    else:
        print("Database already exists")
    
def Create_Row(Database, *Lines):
    path = directory + "Database/" + Database + "/"
    f = open(path + "0000/0000.txt")
    col1 = len(f.readlines())
    col2 = len(Lines)
    if col1 == col2 + 1:
        filesn = len(os.listdir(path))
        os.mkdir(directory + "Database/" + Database + "/" + str(filesn).zfill(4))
        f = open(path + str(filesn).zfill(4) + "/" + str(filesn).zfill(4)  + ".txt", "w+")
        f.write(str(filesn)+ "\n")
        WriteWithNewLine(Lines, f)
    else:
        raise NameError('This table has ' + str(col1) + " columns" + ", you entered " + str(col2) + " columns.")

def Del_Row():
    print("")

def ViewDatabase(Database):
    path = directory + "Database/" + Database + "/"
    files = os.listdir(path)
    filesn = len(files)
    row = []
    for i,file in zip(range(filesn), files):
        file = file + "/" + file[-4:-1] + file[-1] + ".txt"
        f = open(path + file, "r+")
        if i == 0:
            header = list(s.rstrip() for s in (f.readlines()))
        else:
            row.append(list(s.rstrip() for s in (f.readlines())))
    print(tabulate(row,headers = header,tablefmt='orgtbl'))

def GetDatabase(Database):
    path = directory + "Database/" + Database + "/"
    files = os.listdir(path)
    filesn = len(files)
    AllIn = []
    for file in files:
        file = path + file + "/" + file[-4:-1] + file[-1] + ".txt"
        f = open(file, "r+")
        AllIn.append(list(s.rstrip() for s in (f.readlines())))
    return AllIn

def ChangeHisOrHer(Database, Username, ToChange, Into):
    path = "Database/" + Database + "/"
    files = os.listdir(path)
    file = path + files[Username] + "/" + files[Username] + ".txt" 
    replace_line(file, ToChange, Into)
    print(file)

def Del_DB(Database):
    print("")

#FILE_EXPLORER---------------------------------------------------------------------
def GetFilesFolders_D(Folder):
    path = directory + Folder + "/"
    files = os.listdir(path)
    filesn = len(files)
    files = [path + s for s in files]
    return (sorted(files))

def GetFilesFolders(Folder):
    path = directory + Folder + "/"
    path2 = Folder + "/"
    files = os.listdir(path)
    filesn = len(files)
    files = [path2 + s for s in files]
    return (sorted(files))

def GetFilesofType_D(Folder, Type):
    path = directory + Folder + "/"
    filelist = os.listdir(path)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(Type)):
            filelist.remove(fichier)
    files =[path + s for s in filelist]
    return (sorted(files))

def GetFilesofType(Folder, Type):
    path = directory + Folder + "/"
    path2 = Folder + "/"
    filelist = os.listdir(path)
    print(filelist)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(Type)):
            filelist.remove(fichier)
    files =[path2 + s for s in filelist]
    return (sorted(filelist))

def GetFoldersOnly_D(Folder):
    path = directory + Folder + "/"
    files = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f)) ]
    files =[path + s for s in files]
    return (sorted(files))

def GetFoldersOnly(Folder):
    path = directory + Folder + "/"
    path2 = Folder + "/"
    files = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f)) ]
    files =[path2 + s for s in files]
    return (sorted(files))

def GetFilesOnly_D(Folder):
    path = directory + Folder + "/"
    files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
    files =[path + s for s in files]
    return (sorted(files))

def GetFilesOnly(Folder):
    path = directory + Folder + "/"
    path2 = Folder + "/"
    files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
    files =[path2 + s for s in files]
    return (sorted(files))

def MakeDir_D(directoryList):
    for Adirectory in directoryList:
        try:
            os.mkdir(directory+ Adirectory)
        except:
            pass

def MakeDir(directoryList):
    for Adirectory in directoryList:
        try:
            os.mkdir(Adirectory)
        except:
            pass
        
def Delete_D(directoryList, fileList):
    for Adirectory in directoryList:
        try:
            shutil.rmtree(directory + Adirectory)
        except:
            pass
        
    for file in fileList:
        try:
            os.remove(directory + file)
        except:
            pass

def Delete(directoryList, fileList):
    for Adirectory in directoryList:
        try:
            shutil.rmtree(Adirectory)
        except:
            pass
        
    for file in fileList:
        try:
            os.remove(file)
        except:
            pass
        
def DeleteDirContents_D(Directory, directoryList, fileList):
    for Adirectory in directoryList:
        try:
            shutil.rmtree(directory + Directory + "/" + Adirectory)
        except:
            pass
        
    for file in fileList:
        try:
            os.remove(directory + Directory + "/" +  file)
        except:
            pass

def DeleteDirContents(Directory, directoryList, fileList):
    for Adirectory in directoryList:
        try:
            shutil.rmtree(Directory + "/" + Adirectory)
        except:
            pass
        
    for file in fileList:
        try:
            os.remove(Directory + "/" +  file)
        except:
            pass

#Tkinter---------------------------------------------------------------------------
class ScrollableFrame(tk.Frame):
    def __init__(self, container,bgs,sb_bg,arrow, width, height, sb_width, *args, **kwargs):
        super().__init__(container,*args, **kwargs)
        canvas = tk.Canvas(self,height=height,width=width-sb_width,bg=bgs,bd=1,highlightbackground="black")
        
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview,troughcolor=arrow,activebackground="white",bg=sb_bg,width=sb_width)
        self.scrollable_frame = tk.Frame(canvas,bg=bgs,bd=1)
        self.scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw",width=width-sb_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def tkShow(Label, Image_Input, Percentage):
  Img = cv2.imread(directory + Image_Input)
  h,w = Img.shape[:2]
  h = int(h*Percentage)
  Img = imutils.resize(Img, height=h)
  cv2.imwrite("IMGSome.jpg", Img)
  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

from PIL import Image, ImageDraw, ImageFont

def tkShowCropped(Label, Image_Input, X, Y, text):
  Img = cv2.imread(directory + Image_Input)

  h,w = Img.shape[:2]

  Img = Img[Y:100, X:100]

  Img = Image.fromarray(Img)
  fnt = ImageFont.truetype('arial.ttf', 15)
  d = ImageDraw.Draw(Img)
  d.text((0,0), "Hello World", font=fnt, fill=(0,0,0))
  Img.save("IMGSome.jpg")

  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

def PutTextOnImage(X,Y,String,IMG):
  Img = Image.fromarray(IMG)
  fnt = ImageFont.truetype('arial.ttf', 15)

  d = ImageDraw.Draw(Img)
  d.text((X,Y), String, font=fnt, fill=(0,0,0))

  Img.save("IMGSome.png")
  Img = cv2.imread("IMGSome.png")

  return Img

def tkShowWidth(Label, Image_Input, Width):
  Img = cv2.imread(directory + Image_Input)

  Img = imutils.resize(Img, width=Width)
  cv2.imwrite("IMGSome.jpg", Img)
  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

def tkShowHeight(Label, Image_Input, Height):
  Img = cv2.imread(directory + Image_Input)

  Img = imutils.resize(Img, height=Height)
  cv2.imwrite("IMGSome.jpg", Img)
  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

def tkShowCrop(Label, Image_Input, RangeX1,RangeY1, RangeX2, RangeY2, Percentage):
  Img = cv2.imread(directory + Image_Input)

  Img = Img[RangeY1:RangeY2, RangeX1:RangeX2]
  h,w = Img.shape[:2]
  h = int(h*Percentage)
  Img = imutils.resize(Img, height=h)
  cv2.imwrite("IMGSome.jpg", Img)
  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

def tkEntrySetValue(EntryA, Value):
    EntryA.delete(0, tk.END)
    EntryA.insert(0,Value)

#OPENCV----------------------------------------------------------------------
def Rotate_Bound(image, angle):
    # grab the dimensions of the image and then determine the
    # centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def Flip_Image_Horizontally(image):
    return cv2.flip(image, 1)

def Flip_Image_Vertically(image):
    return cv2.flip(image, 0)

def Flip_Image_Along_Origin(image):
    return cv2.flip(image, -1)

def Crop_Image(image, X1,X2,Y1,Y2):
    return image[Y1:Y2, X1:X2]

def PutText(image, text, output_file_name, coordinates, font_size, weight, color):
    img = cv2.imread(directory + image)
    cv2.putText(img,text,coordinates, cv2.FONT_HERSHEY_SIMPLEX, font_size,color,weight,cv2.LINE_AA)
    cv2.imwrite(directory + output_file_name, img)
  
#MISC------------------------------------------------------------------------------
def DuplicateFile(Filename, outputFilename):
    Filename = directory+Filename
    outputFilename = directory+outputFilename
    try:
        print(os.stat(Filename).st_size)
        if (os.stat(Filename).st_size>0):
            shutil.copy(Filename, outputFilename)
        else:
            pass
    except:
        pass

def FloatToString(Number, LeadingZeroes, TrailingZeroes):
    Number=str(Number)
    New_Text = Number.zfill(LeadingZeroes)
    if TrailingZeroes != 0:
        New_Text = New_Text + "."
    for i in range(TrailingZeroes):
        New_Text = New_Text + "0"
    return New_Text

def FindIndexOf(String, List):
    Index = -1
    for i in range(len(List)):
        if (String == List[i]):
            Index = i
            break
    return Index

def GetIndexHighestValue(List):
    Previous = 0
    index = 0
    for i in range(len(List)):
        Current = List[i]
        print(Current,Previous)
        if Current > Previous:
            print("Updated")
            index = i
            Previous = Current
    return index

def GetINFO(Info, Header1, Header2):
  Output=''
  try:
    Info = re.search(Header1 + '(.+?)' + Header2, Info)
    if Info:
      Output = str(Info.group(1))
    if Output=='':
      Output=' '
  except:
    Output = ''
  return Output

def StringListToList(String, separator):
    Strings = list(String)
    NewStrings = []
    NewString = ""
    i = 0
    for s in Strings:
        if s == separator:
            NewStrings.append(NewString)
            NewString = ""
        elif i+1 == len(Strings):
            NewString = NewString + s
            NewStrings.append(NewString)
        else:
            NewString = NewString + s
        i = i+1
    return NewStrings

def greet(Data,*Names):
    for Name in Names:
        print("Hello", Name)

def imread(file_name):
    return cv2.imread(directory + file_name)

def imwrite(file_name, img):
    cv2.imwrite(directory + file_name,img)

def Create_White_Screen(Output_File, DimX, DimY):
    img = np.ones((DimY, DimX,3))*int(255)
    imwrite(Output_File,img)

def Create_Black_Screen(Output_File, DimX, DimY):
    img = np.zeros((DimY, DimX,3))*int(255)
    imwrite(Output_File,img)

def Create_Color_Screen(Output_File, DimX, DimY, R, G, B):
    img = np.zeros([DimY, DimX, 3], dtype=np.uint8)
    img[:,:] = [R, G, B]
    imwrite(Output_File,img)

def MaskImageToAnotherImage(MaskedFileName,img1, img2):
    img1 = imread(img1)
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = imread(img2)
    
    ret, img1 = cv2.threshold(img1,127,255,cv2.THRESH_BINARY)

    masked = cv2.bitwise_or(img2, img2, mask = img1)
    masked[np.where((masked==[0,0,0]).all(axis=2))] = [255,255,255]
    imwrite(MaskedFileName, masked)

def Get_Dimensions(img):
    if type(img) == str:
        img = cv2.imread(img)
        h, w = img.shape[:2]
        return w, h
    else:
        h, w = img.shape[:2]
        return w, h

#TIME FUNCTIONS -------------------------------------------
def SetStartDay():
    f = open("Start.txt", "w+")
    f.write(str(time.time()))

def GetDifferenceSecs():
    return time.time() - float((Read_Text_File("Start.txt"))[0][0])


def GetParamsOfSeconds(x):
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    d,h,m,s = int(d),int(h),int(m),int(s)
    z = ("%02d:%02d:%02d:%02d" %(d,h,m,s))
    return d,h,m,s,z

#ARDUINO --------------------------------------------------
def SendToArduino(StringToSend):
    SerialData.write(bytes(StringToSend, "utf-8"))
    time.sleep(1)
    x = SerialData.read().decode("utf-8")
    while (x != 'D'):
        x = SerialData.read().decode("utf-8")
        print(x)

def SendOnly(StringToSend):
    SerialData.write(bytes(StringToSend, "utf-8"))
    time.sleep(2)

def ParseInfoFromArduino(StringToSend):
    SerialData.write(bytes(StringToSend, "utf-8"))
    time.sleep(1)
    x = SerialData.read().decode("utf-8")
    while (x != 'D'):
        x = SerialData.read().decode("utf-8")
        print(x)

######Create_DB("Alih", "Names", "RFID", "Age")
######Create_Row("Alih", "Gaara", "5634", "34")
######ViewDatabase("Alih")
######print(GetDatabase("Alih"))
######ChangeHisOrHer("Alih", 2, 2, "456754765")
######
######Replace_Line("Hello.txt", 1, "Changed")
######print(GetFilesFolders("Database/Alih/0001"))
######print(GetFilesofType("Database/Alih/0001", ".png"))
######print(GetFoldersOnly("Database/Alih"))
######print(GetFilesOnly("Database/Alih/0001"))
######
######MakeDir(["Alih1234","hehe"])
######Delete(["Alih1234","hehe"],["1.txt"])
######DeleteDirContents("Alih123",["Alih","Alih1"],["Sheehan1.txt","Sheehan.txt"])
######
######Get_Dimensions(capt)
######PutText(image="Box.png", text="Sold Out", output_file_name="Output.png", coordinates=(0,200),font_size=5,weight=5,color=(0, 0, 255))
######Create_White_Screen("Blank.png", 1000, 300)
######Create_Black_Screen("Blank.png", 1000, 300)
######rotate_bound(capt, 90)

######print(FloatToString(1, 2, 0))
######print(Read_Text_File("hey.txt"))
######DuplicateFile("1.txt", "Admin.txt")
######cv2.imshow("z",Flip_Image_Vertically(cv2.imread("bg.png")))
######cv2.imshow("z",Crop_Image(cv2.imread("bg.png"),300,400,300,400))
######cv2.imshow("z",Crop_Image(cv2.imread("bg.png"),300,400,300,400))
######Create_Color_Screen("Hello.png", 100,100, 128,128,128)



def Functio():
    IF.Create_DB("Alih", "Names", "RFID", "Age")
    IF.Create_Row("Alih", "Gaara", "5634", "34")
    IF.ViewDatabase("Alih")
    IF.print(GetDatabase("Alih"))
    IF.ChangeHisOrHer("Alih", 2, 2, "456754765")
    IF.Replace_Line("Hello.txt", 1, "Changed")
    IF.print(GetFilesFolders("Database/Alih/0001"))
    IF.print(GetFilesofType("Database/Alih/0001", ".png"))
    IF.print(GetFoldersOnly("Database/Alih"))
    IF.print(GetFilesOnly("Database/Alih/0001"))
    IF.print(FloatToString(1, 2, 0))
    IF.MakeDir(["Alih1234","hehe"])
    IF.Delete(["Alih1234","hehe"],["1.txt"])
    IF.DeleteDirContents("Alih123",["Alih","Alih1"],["Sheehan1.txt","Sheehan.txt"])
    IF.PutText(image="Box.png", text="Sold Out", output_file_name="Output.png", coordinates=(0,200),font_size=5,weight=5,color=(0, 0, 255))
    IF.Create_White_Screen("Blank.png", 1000, 300)
    IF.Create_Black_Screen("Blank.png", 1000, 300)
    IF.Get_Dimensions
    IF.Rotate_Bound(capt, 90)
