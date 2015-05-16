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

    #(this_file_name, this_file_extension) = os.path.splitext(filename)

    file = default_storage.save('tmp/'+uuid.uuid4().hex+"."+file_extension, ContentFile(uploadFile.read()))
    #fileObject = os.path.join(settings.MEDIA_ROOT, path)

    totalErrors = list()

    #for fileObject in fileObjects:

    # Initialise a new parser from the HTMLParser class
    parser = MyHTMLParserV2()
    fileObject = open(file, 'r')
    
    # Extract the extension from the file object
    #extension = os.path.splitext(fileObject)[-1].lower()

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

        for file in nameList:

            name = file.filename
            
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
                currentFolder.children.append(currentFile.as_json());
                allZipFiles.append(file)
            # is Folder
            else:
                # needs support for subfolders
                zipStructure.append(currentFolder)
                currentFolder = ThorFolder()
                currentFolder.name = name

        # totalErrors.append()

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
                    totalErrors.append(errors)
                except KeyError:
                    continue
                # else:
                    # errors = initialiseErrors(fileObject)
                    # data = fileObject.read()
                    # # This function parses the file and places the results in its class variables
                    # parser.parse(data)
                    # # These variables are then extracted into the errors framework from initialiseErrors()
                    # errors['syntaxErrors'] = parser.syntaxErrors
                    # errors['semanticErrors'] = parser.semanticErrors
                    # errors['deprecatedErrors'] = parser.deprecatedErrors
                    # errors['practiceErrors'] = parser.practiceErrors
                    # totalErrors.append(errors)

        return { "structure": [ob.as_json() for ob in zipStructure], "errors": totalErrors }

    return totalErrors

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
    return totalErrors

def initialiseErrors(fileObject):
    errors = { 'fileName':fileObject,
               'syntaxErrors':{},
               'semanticErrors':{},
               'deprecatedErrors':{},
               'practiceErrors':{},
               'sourceCode':[] }
    return errors
    











