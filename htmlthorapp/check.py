import os
import zipfile
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from htmlparser import MyHTMLParser
from htmlparser2 import MyHTMLParserV2

def checkFile(uploadFile, file_extension):

    #(this_file_name, this_file_extension) = os.path.splitext(filename)

    file = default_storage.save('tmp/'+uuid.uuid4().hex+"."+file_extension, ContentFile(uploadFile.read()))
    #fileObject = os.path.join(settings.MEDIA_ROOT, path)

    totalErrors = list()

    #for fileObject in fileObjects:

    # Initialise a new parser from the HTMLParser class
    parser = MyHTMLParserV2()
    
    # Extract the extension from the file object
    #extension = os.path.splitext(fileObject)[-1].lower()

    # If it is a single file, simply parse it
    # Treat a .php file the same as a .html file
    # as the parsing function ignores script and php tags
    if (file_extension == "html" or file_extension == "php"):

        fileObject = open(file, 'r')

        errors = initialiseErrors(fileObject)
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
    elif this_file_extension == ".zip":
        zipFile = zipfile.ZipFile(fileObject, 'r')
        nameList = zipFile.namelist()
        for name in nameList:
            if(os.path.splitext(name)[-1].lower()==".html" or os.path.splitext(name)[-1].lower()==".php"):
                try:
                    data = zipFile.read(name)
                except KeyError:
                    continue
                else:
                    errors = initialiseErrors(fileObject)
                    data = fileObject.read()
                    # This function parses the file and places the results in its class variables
                    parser.parse(data)
                    # These variables are then extracted into the errors framework from initialiseErrors()
                    errors['syntaxErrors'] = parser.syntaxErrors
                    errors['semanticErrors'] = parser.semanticErrors
                    errors['deprecatedErrors'] = parser.deprecatedErrors
                    errors['practiceErrors'] = parser.practiceErrors
                    totalErrors.append(errors)

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
    errors = { 'fileName':str(fileObject),
               'syntaxErrors':{},
               'semanticErrors':{},
               'deprecatedErrors':{},
               'practiceErrors':{},
               'sourceCode':[] }
    return errors
    











