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
        self.path = ""
        self.children = list()
        self.children_parsed = list()

    def as_json(self):
        # self.json_children(self.children)
        return { "type": self.type, 
                 "name": self.name, 
                 "children": self.children_parsed }

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

zipFileStructure = list()
rootFolder = ThorFolder()

# Create folder structure given a folder path
def createFolder(folders):

    if (folders.find("__MACOSX") == 0):
        return

    nameList = folders.split("/")
    depth = 0
    previousFolder = rootFolder

    for name in nameList:
        
        folder = ThorFolder()
        folder.name = name

        path = nameList[0] + "/"
        k = 1
        while (k < depth):
            path = path + nameList[k] + "/"
            k+=1

        folder.path = path

        previousFolder.children.append(folder)
        previousFolder.children_parsed.append(folder.as_json())
        
        previousFolder = folder
        depth+=1

# Find folder given path
def findFolder(folders, path):

    foundFolder = ThorFolder()

    for folder in folders:
        if (folder.type == "folder"):
            if (folder.path == path):
                return folder
            elif (len(folder.children) > 0):
                foundFolder = findFolder(folder.children, path)

    return foundFolder


# Add file to specific folder path
def addFileToFolder(file):

    path = file.split("/")
    del path[-1];
    path = '/'.join(path) + "/"
    folder = findFolder(zipFileStructure, path)

    currentFile = ThorFile()
    currentFile.name = file.split("/")[-1]
    currentFile.extension = os.path.splitext(file)[-1].lower()
    
    # If CSS is outside of CSS or Styles folder
    if (currentFile.extension == ".css" and folder.name != "css"):
        currentFile.locationBad = True

    # If JS is outside of JS or Javascript folder
    if (currentFile.extension == ".js" and folder.name != "js"):
        currentFile.locationBad = True

    folder.children.append(currentFile);
    folder.children_parsed.append(currentFile.as_json())

    return

def checkFile(uploadFile, file_extension):
    
    global zipFileStructure
    global rootFolder

    uploaded_file = default_storage.save('tmp/'+uuid.uuid4().hex+"."+file_extension, ContentFile(uploadFile.read()))

    totalErrors = list()

    # Initialise a new parser from the HTMLParser class
    parser = MyHTMLParserV2()
    fileObject = open(uploaded_file, 'r')

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

        allZipFiles = list()

        print "Hello!"
        # Reset zip structure
        zipFileStructure = list()
        rootFolder = ThorFolder()
        rootFolder.name = "root"
        rootFolder.path = "/"
        zipFileStructure.append(rootFolder)

        for file in nameList:

            name = file.filename
            
            # Create folders
            if (file.file_size == 0):
                createFolder(name)

        for file in nameList:

            name = file.filename
            
            # Add file to folder
            if (file.file_size > 0 and name.find("__MACOSX") == -1 and name.find(".DS_Store") == -1):
                addFileToFolder(name)
                allZipFiles.append(file)

        for file in allZipFiles:
            
            name = file.filename
            # print name

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

        # deletes uploaded file and returns errors
        #default_storage.delete(file)
        #return { "structure": [ob.as_json() for ob in zipFileStructure], "errors": totalErrors }

    # deletes uploaded file and returns errors
    default_storage.delete(uploaded_file)

    if (len(zipFileStructure) > 0):
        return { "structure": [ob.as_json() for ob in zipFileStructure], "errors": totalErrors }
    else:
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
    











