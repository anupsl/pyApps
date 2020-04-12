import bs4
from src.Constant.constant import constant
from src.utilities.logger import Logger

class FileHelper():
    
    def __init__(self, filePath):
        self.filePath = filePath
        open(self.filePath, 'w')
                    
    def writeFile(self, data):
        fileObject = open(self.filePath, 'w+')
        try:
            fileObject.write(data)
        except Exception, exp:
            Logger.log('Exception Occured while Writing to File :', exp)
        finally:
            fileObject.close()
            
    def eraseContentFromFile(self):
        try:
            open(self.filePath, 'w').close()
        except Exception, exp:
            Logger.log('Exception Occured while Erasing Content From File')
            
    def appendToFile(self, data):
        fileObject = open(self.filePath, 'a')
        try:
            fileObject.write(data + '\n')
        except:
            Logger.log('Exception Occured while Appending to File')
        finally:
            fileObject.close()
            
    @staticmethod
    def concateHTMLandCSS():
        path = constant.config['logDir']
        htmlFilePath = path + '/result.html'
        styleFile = path + '/assets/style.css'
        outputFile = path + '/output.html'        
        soup = bs4.BeautifulSoup(open(htmlFilePath).read(), "lxml")
        stylesheets = soup.findAll("link", {"rel": "stylesheet"})
        for s in stylesheets:
            t = soup.new_tag('style')
            c = bs4.element.NavigableString(open(styleFile).read())
            t.insert(0, c)
            t['type'] = 'text/css'
            s.replaceWith(t)
        open(outputFile, "w").write(str(soup).replace('&amp;apos;', ''))
        Logger.logCollectorRequest(outputFile, 'files')


    @staticmethod
    def readFile(filePath):
        fh = open(filePath, 'r+')
        body = fh.read()
        fh.close()
        return body    
