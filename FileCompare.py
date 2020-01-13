import os
import hashlib
import string
import wx
import wx.xrc

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"源目录", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrlSrcDir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,30 ), 0 )
        bSizer2.Add( self.m_textCtrlSrcDir, 0, wx.ALL, 5 )

        self.m_buttonSrc = wx.Button( self, wx.ID_ANY, u"选择源目录", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_buttonSrc, 0, wx.ALL, 5 )

        self.m_buttonCompare = wx.Button(self, wx.ID_ANY, u"开始比较", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_buttonCompare, 0, wx.ALL, 5)


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"目的目录1", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer21.Add( self.m_staticText11, 0, wx.ALL, 5 )

        self.m_textCtrlDesDir1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 420,30 ), 0 )
        bSizer21.Add( self.m_textCtrlDesDir1, 0, wx.ALL, 5 )

        self.m_buttonDes1 = wx.Button( self, wx.ID_ANY, u"选择目的目录1", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.m_buttonDes1, 0, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"MD5相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer21.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer21.Add( self.m_staticText11, 0, wx.ALL, 5 )

        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"文件名相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        bSizer21.Add( self.m_staticText10, 0, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        bSizer21.Add( self.m_staticText12, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

        m_buttonDes1 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"目的目录2", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText111.Wrap( -1 )

        m_buttonDes1.Add( self.m_staticText111, 0, wx.ALL, 5 )

        self.m_textCtrlDesDir2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 420,30 ), 0 )
        m_buttonDes1.Add( self.m_textCtrlDesDir2, 0, wx.ALL, 5 )

        self.m_buttonDes2 = wx.Button( self, wx.ID_ANY, u"选择目的目录2", wx.DefaultPosition, wx.DefaultSize, 0 )
        m_buttonDes1.Add( self.m_buttonDes2, 0, wx.ALL, 5 )

        self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"MD5相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )

        m_buttonDes1.Add( self.m_staticText61, 0, wx.ALL, 5 )

        self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        m_buttonDes1.Add( self.m_staticText21, 0, wx.ALL, 5 )

        self.m_staticText101 = wx.StaticText( self, wx.ID_ANY, u"文件名相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText101.Wrap( -1 )

        m_buttonDes1.Add( self.m_staticText101, 0, wx.ALL, 5 )

        self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )

        m_buttonDes1.Add( self.m_staticText22, 0, wx.ALL, 5 )


        bSizer1.Add( m_buttonDes1, 1, wx.EXPAND, 5 )

        bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText113 = wx.StaticText( self, wx.ID_ANY, u"目的目录3", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText113.Wrap( -1 )

        bSizer211.Add( self.m_staticText113, 0, wx.ALL, 5 )

        self.m_textCtrlDesDir3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 420,30 ), 0 )
        bSizer211.Add( self.m_textCtrlDesDir3, 0, wx.ALL, 5 )

        self.m_buttonDes3 = wx.Button( self, wx.ID_ANY, u"选择目的目录3", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer211.Add( self.m_buttonDes3, 0, wx.ALL, 5 )

        self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"MD5相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )

        bSizer211.Add( self.m_staticText62, 0, wx.ALL, 5 )

        self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31.Wrap( -1 )

        bSizer211.Add( self.m_staticText31, 0, wx.ALL, 5 )

        self.m_staticText102 = wx.StaticText( self, wx.ID_ANY, u"文件名相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText102.Wrap( -1 )

        bSizer211.Add( self.m_staticText102, 0, wx.ALL, 5 )

        self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText32.Wrap( -1 )

        bSizer211.Add( self.m_staticText32, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )

        bSizer212 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText115 = wx.StaticText( self, wx.ID_ANY, u"目的目录4", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText115.Wrap( -1 )

        bSizer212.Add( self.m_staticText115, 0, wx.ALL, 5 )

        self.m_textCtrlDesDir4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 420,30 ), 0 )
        bSizer212.Add( self.m_textCtrlDesDir4, 0, wx.ALL, 5 )

        self.m_buttonDes4 = wx.Button( self, wx.ID_ANY, u"选择目的目录4", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer212.Add( self.m_buttonDes4, 0, wx.ALL, 5 )

        self.m_staticText63 = wx.StaticText( self, wx.ID_ANY, u"MD5相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText63.Wrap( -1 )

        bSizer212.Add( self.m_staticText63, 0, wx.ALL, 5 )

        self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )

        bSizer212.Add( self.m_staticText41, 0, wx.ALL, 5 )

        self.m_staticText103 = wx.StaticText( self, wx.ID_ANY, u"文件名相似度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText103.Wrap( -1 )

        bSizer212.Add( self.m_staticText103, 0, wx.ALL, 5 )

        self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText42.Wrap( -1 )

        bSizer212.Add( self.m_staticText42, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer212, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        self.m_buttonSrc.Bind(wx.EVT_BUTTON, self.open, self.m_buttonSrc)
        self.m_buttonDes1.Bind(wx.EVT_BUTTON, self.open, self.m_buttonDes1)
        self.m_buttonDes2.Bind(wx.EVT_BUTTON, self.open, self.m_buttonDes2)
        self.m_buttonDes3.Bind(wx.EVT_BUTTON, self.open, self.m_buttonDes3)
        self.m_buttonDes4.Bind(wx.EVT_BUTTON, self.open, self.m_buttonDes4)
        self.m_buttonCompare.Bind(wx.EVT_BUTTON, self.compare, self.m_buttonCompare)

    def __del__( self ):
        pass

    def open(self, event):
        # 弹出目录选择对话框
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            name = event.GetEventObject().GetLabel()
            if name == "选择源目录":
                self.m_textCtrlSrcDir.SetValue(dlg.GetPath())
            elif name == "选择目的目录1":
                self.m_textCtrlDesDir1.SetValue(dlg.GetPath())
            elif name == "选择目的目录2":
                self.m_textCtrlDesDir2.SetValue(dlg.GetPath())
            elif name == "选择目的目录3":
                self.m_textCtrlDesDir3.SetValue(dlg.GetPath())
            elif name == "选择目的目录4":
                self.m_textCtrlDesDir4.SetValue(dlg.GetPath())
            dlg.Destroy()

    # 遍历某个文件夹下面所有的文件，把文件的全路径名放到列表中
    def getAllFilesFromDir(self,dirPath):
        filePathList = []
        for root, dirs, files in os.walk(dirPath):
            #root 当前目录路径
            #dirs 当前路径下所有子目录
            #files 当前路径下所有非目录子文件
            for file in files:
                filePath = os.path.join(root,file)
                filePathList.append(filePath)
        print("dir "+dirPath+"  has "+ str(len(filePathList))+"  files")
        return  filePathList

    # 获取单个文件的MD5码
    def getMD5(self, file):
        m = hashlib.md5()
        with open(file, 'rb') as f:
            for line in f:
                m.update(line)
        md5code = m.hexdigest()
        return md5code

    # 从一个文件列表中获取其对应的文件md5，并按列表方式返回
    def getMD5FromFileList(self, filePathList):
        fileMD5List = []
        for filePath in filePathList:
            fileMD5List.append(self.getMD5(filePath))
        return fileMD5List

    # 通过md5码的方式比较两个list的相似度
    def compareFileListByMD5(self, md5List1, md5List2):
        len1 = len(md5List1)
        len2 = len(md5List2)
        i= 0
        for md5code in md5List1:
            if md5code in md5List2:
                i = i+1
        result1 = i / (len1)
        result2 = i / (len2)
        result3 = i /(i+len1-i+len2-i)
        return [result1,result2,result3]

    # 通过文件相对路径名的方式比较两个list的相似度
    def compareFileListByFilename(self, filePathList1, filePathList2):
        len1 = len(filePathList1)
        len2 = len(filePathList2)
        i= 0
        for filename in filePathList1:
            if filename in filePathList2:
                i = i+1
        result1 = i / (len1)
        result2 = i / (len2)
        result3 = i /(i+len1-i+len2-i)
        return [result1,result2,result3]

    # 去掉文件夹的根目录，这样才好比较
    def removeRootDirname(self, filePathList, rootdir):
        newList = []
        for filePath in filePathList:
            if filePath.startswith(rootdir):
                newList.append(filePath[len(rootdir):])
        return newList


    def compare(self, event):

        dirSrcPath = self.m_textCtrlSrcDir.GetValue()
        dirDesPath1 = self.m_textCtrlDesDir1.GetValue()
        dirDesPath2 = self.m_textCtrlDesDir2.GetValue()
        dirDesPath3 = self.m_textCtrlDesDir3.GetValue()
        dirDesPath4 = self.m_textCtrlDesDir4.GetValue()

        filePathListSrc =  self.getAllFilesFromDir(dirSrcPath)
        filePathListDes1 = self.getAllFilesFromDir(dirDesPath1)
        filePathListDes2 = self.getAllFilesFromDir(dirDesPath2)
        filePathListDes3 = self.getAllFilesFromDir(dirDesPath3)
        filePathListDes4 = self.getAllFilesFromDir(dirDesPath4)

        if(len(filePathListSrc)) < 1:
            return

        md5ListSrc = self.getMD5FromFileList(filePathListSrc)
        filePathListSrc = self.removeRootDirname(filePathListSrc, dirSrcPath)

        if(len(filePathListDes1)) > 1:
            md5ListDes1 = self.getMD5FromFileList(filePathListDes1)
            res1 = self.compareFileListByMD5(md5ListSrc, md5ListDes1)
            percent11 = "%.1f%%" % (res1[0] * 100)
            print(res1)
            if(res1[0] > 0.5):
                self.m_staticText11.SetBackgroundColour('Red')
            elif (res1[0] < 0.2):
                self.m_staticText11.SetBackgroundColour('Green')
            self.m_staticText11.SetLabel(percent11)

            filePathListDes1 = self.removeRootDirname(filePathListDes1, dirDesPath1)
            res2 = self.compareFileListByFilename(filePathListSrc, filePathListDes1)
            percent12 = "%.1f%%" % (res2[0] * 100)
            print(res2)
            if(res2[0] > 0.5):
                self.m_staticText12.SetBackgroundColour('Red')
            elif (res2[0] < 0.2):
                self.m_staticText12.SetBackgroundColour('Green')
            self.m_staticText12.SetLabel(percent12)

        if(len(filePathListDes2)) > 1:
            print(dirDesPath2)
            md5ListDes2 = self.getMD5FromFileList(filePathListDes2)
            res1 = self.compareFileListByMD5(md5ListSrc, md5ListDes2)
            percent21 = "%.1f%%" % (res1[0] * 100)
            print(res1)
            if(res1[0] > 0.5):
                self.m_staticText21.SetBackgroundColour('Red')
            elif (res1[0] < 0.2):
                self.m_staticText21.SetBackgroundColour('Green')
            self.m_staticText21.SetLabel(percent21)

            print(len(filePathListDes2))
            filePathListDes2 = self.removeRootDirname(filePathListDes2, dirDesPath2)
            res2 = self.compareFileListByFilename(filePathListSrc, filePathListDes2)
            percent22 = "%.1f%%" % (res2[0] * 100)
            print(res2)
            if(res2[0] > 0.5):
                self.m_staticText22.SetBackgroundColour('Red')
            elif (res2[0] < 0.2):
                self.m_staticText22.SetBackgroundColour('Green')
            self.m_staticText22.SetLabel(percent22)

        if(len(filePathListDes3)) > 1:
            md5ListDes3 = self.getMD5FromFileList(filePathListDes3)
            res1 = self.compareFileListByMD5(md5ListSrc, md5ListDes3)
            percent31 = "%.1f%%" % (res1[0] * 100)
            print(res1)
            if(res1[0] > 0.5):
                self.m_staticText31.SetBackgroundColour('Red')
            elif (res1[0] < 0.2):
                self.m_staticText31.SetBackgroundColour('Green')
            self.m_staticText31.SetLabel(percent31)

            filePathListDes3 = self.removeRootDirname(filePathListDes3, dirDesPath3)
            res2 = self.compareFileListByFilename(filePathListSrc, filePathListDes3)
            percent32 = "%.1f%%" % (res2[0] * 100)
            print(res2)
            if (res2[0] > 0.5):
                self.m_staticText32.SetBackgroundColour('Red')
            elif (res2[0] < 0.2):
                self.m_staticText32.SetBackgroundColour('Green')
            self.m_staticText32.SetLabel(percent32)

        if(len(filePathListDes4)) > 1:
            md5ListDes4 = self.getMD5FromFileList(filePathListDes4)
            res1 = self.compareFileListByMD5(md5ListSrc, md5ListDes4)
            percent41 = "%.1f%%" % (res1[0] * 100)
            print(res1)
            if(res1[0] > 0.5):
                self.m_staticText41.SetBackgroundColour('Red')
            elif (res1[0] < 0.2):
                self.m_staticText41.SetBackgroundColour('Green')
            self.m_staticText41.SetLabel(percent41)

            filePathListDes4 = self.removeRootDirname(filePathListDes4, dirDesPath4)
            res2 = self.compareFileListByFilename(filePathListSrc, filePathListDes4)
            percent42 = "%.1f%%" % (res2[0] * 100)
            print(res2)
            if (res2[0] > 0.5):
                self.m_staticText42.SetBackgroundColour('Red')
            elif (res2[0] < 0.2):
                self.m_staticText42.SetBackgroundColour('Green')
            self.m_staticText42.SetLabel(percent42)





if __name__=='__main__':
    app = wx.App()  # 创建一个应用程序对象
    frame = MyFrame1(None)
    frame.Show()
    app.MainLoop()






