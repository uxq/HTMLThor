import os
import zipfile
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from htmlparser import MyHTMLParser
from htmlparser2 import MyHTMLParserV2

class ThorFolder:
    def __init__(self):
        self.type = "folder"
        self.name = ""
        self.children = list()

    def as_json(self):
        return { "type": self.type, 
                 "name": self.name, 
                 "children": self.children }

class ThorFile(ThorFolder):
    def __init__(self):
        self.type = "file"
        self.extension = ""
        self.broken = False
        self.brokenCount = 0
        self.locationBad = False

    def as_json(self):
        return { "type": self.type, 
                 "name": self.name, 
                 "extension": self.extension, 
                 "broken": self.broken, 
                 "brokenCount": self.brokenCount, 
                 "locationBad": self.locationBad }

def checkFile(uploadFile, file_extension):

    file = default_storage.save('tmp/'+uuid.uuid4().hex+"."+file_extension, ContentFile(uploadFile.read()))

    totalErrors = list()

    # Initialise a new parser from the HTMLParser class
    parser = MyHTMLParserV2()
    fileObject = open(file, 'r')

    # If it is a single file, simply parse it
    # Treat a .php file the same as a .html file
    # as the parsing function ignores script and php tags
    if (file_extension == "html" or file_extension == "php"):

        errors = initialiseErrors(uploadFile.name)
        """ Might need to open before reading file"""
        data = fileObject.read()
        # This function parses the file and places the results in its class variables
        parser.parse(data)
        # These variables are then extracted into the errors framework from initialiseErrors()
        errors['syntaxErrors'] = parser.syntaxErrors
        errors['semanticErrors'] = parser.semanticErrors
        errors['deprecatedErrors'] = parser.deprecatedErrors
        errors['practiceErrors'] = parser.practiceErrors
        errors['sourceCode'] = str(data).splitlines()
        totalErrors.append(errors)

    # If it is a zip file, extract it and for each file
    # That is either .html or .php, parse them
    elif file_extension == "zip":

        zipFile = zipfile.ZipFile(fileObject, 'r')
        nameList = zipFile.infolist()
        
        zipStructure = list()
        currentFolder = ThorFolder()
        allZipFiles = list()
        isMacOsx = False

        for file in nameList:

            name = file.filename

            # Skip __MACOSX folder
            if (name.find("__MACOSX") == -1):
            
                # File is in root folder
                if (len(name.split("/")) == 1):
                    zipStructure.append(currentFolder)
                    currentFolder = ThorFolder()
                    currentFolder.name = "root"

                # is File
                if (file.file_size > 0):
                    currentFile = ThorFile()
                    currentFile.name = name.split("/")[-1]
                    currentFile.extension = os.path.splitext(name)[-1].lower()
                    
                    # If CSS is outside of CSS or Styles folder
                    if (currentFile.extension == ".css" and currentFolder.name != "css/"):
                        currentFile.locationBad = True

                    # If JS is outside of JS or Javascript folder
                    if (currentFile.extension == ".js" and currentFolder.name != "js/"):
                        currentFile.locationBad = True

                    currentFolder.children.append(currentFile.as_json());
                    allZipFiles.append(file)
                # is Folder
                else:
                    # needs support for subfolders
                    zipStructure.append(currentFolder)
                    currentFolder = ThorFolder()
                    currentFolder.name = name

        for file in allZipFiles:
            
            name = file.filename
            print name

            if(os.path.splitext(name)[-1].lower()==".html" or os.path.splitext(name)[-1].lower()==".php"):
                try:
                    data = zipFile.read(name)
                    errors = initialiseErrors(name.split("/")[-1])
                    # This function parses the file and places the results in its class variables
                    parser.parse(data)
                    # These variables are then extracted into the errors framework from initialiseErrors()
                    errors['syntaxErrors'] = parser.syntaxErrors
                    errors['semanticErrors'] = parser.semanticErrors
                    errors['deprecatedErrors'] = parser.deprecatedErrors
                    errors['practiceErrors'] = parser.practiceErrors
                    errors['sourceCode'] = str(data).splitlines()
                    totalErrors.append(errors)
                except KeyError:
                    continue

        return { "structure": [ob.as_json() for ob in zipStructure], "errors": totalErrors }

    return { "errors": totalErrors }

def checkUrl(data):
    return

def checkDirect(data):
    totalErrors = list()
    errors = initialiseErrors("Direct")
    parser = MyHTMLParserV2()
    parser.parse(str(data))
    errors['syntaxErrors'] = parser.syntaxErrors
    errors['semanticErrors'] = parser.semanticErrors
    errors['deprecatedErrors'] = parser.deprecatedErrors
    errors['practiceErrors'] = parser.practiceErrors
    errors['sourceCode'] = str(data).splitlines()
    totalErrors.append(errors)
    return { "errors": totalErrors }

def initialiseErrors(fileObject):
    errors = { 'fileName':fileObject,
               'syntaxErrors':{},
               'semanticErrors':{},
               'deprecatedErrors':{},
               'practiceErrors':{},
               'sourceCode':[] }
    return errors
    











