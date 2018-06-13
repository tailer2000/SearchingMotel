from tkinter import *
from tkinter import ttk
from tkinter import font
import urllib
import urllib.request

g_Tk = Tk()
g_Tk.title("숙박 업소 찾기")
g_Tk.resizable(0,0)
g_Tk.geometry("970x800+100+100")
DataList = []
url = str("")


def InitTopText():
    TempFont = font.Font(g_Tk, size=30, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="오늘은 늦었다[숙박 검색]")
    MainText.pack()
    MainText.place(x=270)

    global combo

    SearchFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')

    combo = ttk.Combobox(g_Tk, font=SearchFont, width=10, height=1)
    combo['values'] = ('이름 검색', '지역 검색')
    combo.place(x=10, y=70)


def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 73, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=127)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=18, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=870, y=127)

def InitSelectLabel():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')

    selectLabel = Label(g_Tk, bg="white", height=25, width=64, borderwidth = 12, relief = 'ridge') #사진
    selectLabel.pack()
    selectLabel.place(x=470, y=215)

    selectText = Text(g_Tk, width=64, height=7, borderwidth=12, relief='ridge')
    selectText.pack()
    selectText.place(x=470, y=635)

def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0, END)
    c = combo.current()

    if  c == 0:
        GetInfo()
    elif c == 1:
        GetArea()

    RenderText.bind('<<ListboxSelect>>', onselect)


def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    c = combo.current()
    print('You selected item %d: "%s"' % (index, value))

    if c == 0:
        url = DataList.index(value) - 2
        url = DataList[url]
        print(url)

        from io import BytesIO
        from PIL import Image, ImageTk

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        im = Image.open(BytesIO(raw_data))
        ph = ImageTk.PhotoImage(im)

        selectLabel = Label(g_Tk, image=ph, height=375, width=450)
        selectLabel.image = ph
        selectLabel.pack()
        selectLabel.place(x=480, y=225)

        TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
        selectText = Text(g_Tk, width=50, height=5, borderwidth=12, relief='ridge', font = TempFont)

        selectText.insert(INSERT, '숙박지명 : ')
        selectText.insert(INSERT, value)
        selectText.insert(INSERT, "\n")
        selectText.insert(INSERT, '전화 : ')
        selectText.insert(INSERT, DataList[DataList.index(value) - 1])
        selectText.insert(INSERT, "\n")
        selectText.insert(INSERT, '주소 : ')
        selectText.insert(INSERT, DataList[DataList.index(value) - 3])
        selectText.insert(INSERT, "\n")

        selectText.pack()
        selectText.place(x=470, y=635)

    elif c == 1:
        url = DataList.index(value) + 1
        url = DataList[url]
        print(url)

        from io import BytesIO
        from PIL import Image, ImageTk

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        im = Image.open(BytesIO(raw_data))
        ph = ImageTk.PhotoImage(im)

        selectLabel = Label(g_Tk, image=ph, height=375, width=450)
        selectLabel.image = ph
        selectLabel.pack()
        selectLabel.place(x=480, y=225)

        TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
        selectText = Text(g_Tk, width=50, height=5, borderwidth=12, relief='ridge', font=TempFont)

        selectText.insert(INSERT, '숙박지명 : ')
        selectText.insert(INSERT, DataList[DataList.index(value) + 3])
        selectText.insert(INSERT, "\n")
        selectText.insert(INSERT, '전화 : ')
        selectText.insert(INSERT, DataList[DataList.index(value) + 1])
        selectText.insert(INSERT, "\n")
        selectText.insert(INSERT, '주소 : ')
        selectText.insert(INSERT, value)
        selectText.insert(INSERT, "\n")

        selectText.pack()
        selectText.place(x=470, y=635)


def GetInfo():
    import http.client
    from xml.dom.minidom import parse, parseString

    conn = None
    path = InputLabel.get()
    encText = urllib.parse.quote(path)

    server = "api.visitkorea.or.kr"
    servicekey = "QZ8JKaSvORPU%2F0gzUXOjsmxrgd5D59mpLe2WJTl1Ttr7f746Meax%2Fj0wGnyJN4qFLQ%2FJIEz5rxAq3SDI59yLTw%3D%3D"
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/openapi/service/rest/KorService/searchStay?serviceKey=" + servicekey +
        "&numOfRows=5000&pageSize=10&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&listYN=Y")
    req = conn.getresponse()

    if int(req.status) == 200:
        response_body = req.read().decode('utf-8')
        parseData = parseString(response_body)
        GeoInfoWhere = parseData.childNodes
        row = GeoInfoWhere[0].childNodes[1].childNodes[0].childNodes

        global DataList
        DataList.clear()
        for item in row:
            list = item.childNodes
            for l in list:
                if l.nodeName == 'addr1':
                    DataList.append(l.firstChild.nodeValue)
                if l.nodeName == 'firstimage':
                    DataList.append(l.firstChild.nodeValue)
                if l.nodeName == 'tel':
                    DataList.append(l.firstChild.nodeValue)
                if l.nodeName == 'title':
                    DataList.append(l.firstChild.nodeValue)
                    if(l.firstChild.nodeValue.find(path)):
                        pass
                    else:
                        RenderText.insert(END, l.firstChild.nodeValue)
    else:
        print("Error")


def GetArea():
    import http.client
    from xml.dom.minidom import parse, parseString

    conn = None
    path = InputLabel.get()
    encText = urllib.parse.quote(path)

    server = "api.visitkorea.or.kr"
    servicekey = "QZ8JKaSvORPU%2F0gzUXOjsmxrgd5D59mpLe2WJTl1Ttr7f746Meax%2Fj0wGnyJN4qFLQ%2FJIEz5rxAq3SDI59yLTw%3D%3D"
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/openapi/service/rest/KorService/searchStay?serviceKey=" + servicekey +
                 "&numOfRows=5000&pageSize=10&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&listYN=Y")
    req = conn.getresponse()

    print(req)

    if int(req.status) == 200:
        response_body = req.read().decode('utf-8')
        parseData = parseString(response_body)
        GeoInfoWhere = parseData.childNodes
        row = GeoInfoWhere[0].childNodes[1].childNodes[0].childNodes

        global DataList
        DataList.clear()
        for item in row:
            list = item.childNodes
            for l in list:
                if l.nodeName == 'addr1':
                    DataList.append(l.firstChild.nodeValue)
                    if (l.firstChild.nodeValue.find(path)):
                        pass
                    else:
                        RenderText.insert(END, l.firstChild.nodeValue)
                if l.nodeName == 'firstimage':
                    DataList.append(l.firstChild.nodeValue)
                if l.nodeName == 'tel':
                    DataList.append(l.firstChild.nodeValue)
                if l.nodeName == 'title':
                    DataList.append(l.firstChild.nodeValue)
    else:
        print("Error")


def InitRenderText():
    global RenderText

    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    RenderText = Listbox(g_Tk, width=45, height=26, borderwidth=12, relief='ridge', font = TempFont)
    RenderText.pack()
    RenderText.place(x=10, y=215)


InitTopText()
InitInputLabel()
InitSearchButton()
InitRenderText()
InitSelectLabel()
g_Tk.mainloop()