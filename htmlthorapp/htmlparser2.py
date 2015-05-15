'''
HTML Thor Parser V2
Jonathan Holland, Simon Hales, Andrea Epifani
University of Queensland - 2015
'''

from sql import SqlFunctions
from encapsulation import Encapsulation
from HTMLParser import HTMLParser
import re

class ThorTag:
    def __init__(self):
        self.tagName = ""
        self.position = list()

#Extends Python HTMLParser
class MyHTMLParserV2(HTMLParser):
    def __init__(self):
        
        HTMLParser.__init__(self)

        self.syntaxErrors = list()
        self.semanticErrors = list()
        self.deprecatedErrors = list()
        self.practiceErrors = list()

        self.singularTags = list()
        self.requiredTags = list()

        self.openedTag = list()
        self.closedTag = list()
        self.hasDoctype = False
        self.doctypeCount = 0

    def closeTheTag(self):
        self.openDoctype = False
        self.closeTag = True
        self.openTag = False
        self.tag = ""
        self.endTagName = False
        self.tagChecked = False
        self.faultyTag = False

    prevTag = ""

    # Handles Doctype
    def handle_decl(self, decl):

        line, offset = self.getpos()
        sql = SqlFunctions()

        self.hasDoctype = True
        self.doctypeCount = self.doctypeCount + 1

        if (line > 1):
            self.hasDoctype = False

        if (not decl.lower().replace(" ", "") == "doctypehtml"):
            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(2), 'type': "syntax"}
            self.syntaxErrors.append(error)

    # Handles start of tags
    def handle_starttag(self, tag, attributes):

        sql = SqlFunctions()
        line, offset = self.getpos()

        if (len(self.openedTag) > 0):
            prevTag = self.openedTag[-1].tagName
        else:
            prevTag = ""

        # print "Encountered a start tag:", tag
        if (sql.isSelfClosing(tag.lower()) == False):
            thorTag = ThorTag()
            thorTag.tagName = tag
            thorTag.position = (line, offset)
            self.openedTag.append(thorTag)
        
        # Check attributes
        attrList = sql.getAttr(tag.lower())
        not_allowed_class_id = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']

        styleHasRel = False
        styleHasType = False
        scriptHasType = False

        for attribute, value in attributes:

            #check for charset existance
            if(tag.lower() == "meta" and attribute.lower() == "charset" and value.lower() == "utf-8"): 
                self.requiredTags.append(tag.lower())
                break

            validAttr = True if attribute in attrList else False
                                              
            if (attribute[0:5].lower() == "data-"):
                validAttr = True

            if (validAttr and (attribute.lower() == "id" or attribute.lower() == "class")):
                if(any(s in value for s in not_allowed_class_id)):
                    error = {'line': line, 'column': offset, 'message' : "Invalid charactes used in value", 'type': "syntax"} #change from endAttr
                    self.syntaxErrors.append(error)

            if (validAttr and attribute.lower() == "alt" and len(value.replace(" ", "")) < 2):
                error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(36), 'type': "practice"}
                self.practiceErrors.append(error)

            if (tag.lower() == "link" and (validAttr and attribute.lower() == "rel")):
                styleHasRel = True
            if (tag.lower() == "link" and (validAttr and attribute.lower() == "type")):
                styleHasType = True
            if (tag.lower() == "script" and (validAttr and attribute.lower() == "type")):
                scriptHasType = True

            if (validAttr and attribute.lower() == "style"):
                error = {'line': line, 'column': offset, 'message' : "You shouldn't use inline style, use a separate CSS file instead.", 'type': "practice"}
                self.practiceErrors.append(error)

            if (not validAttr):
                debugError = {'line': line, 'column': offset, 'message' : "Not a valid attribute("+attribute+")", 'type': "practice"}
                self.practiceErrors.append(debugError) 
            # lang is valid tag for html as in http://www.w3.org/TR/html5/semantics.html
            elif (attribute.lower() == "lang" and tag.lower() == "html"):
                validAttr = True
            elif (sql.isDeprecatedAttribute(attribute)):
                error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(30).replace("--attr",attribute).replace("--tag",tag), 'type': "deprecated"}
                self.deprecatedErrors.append(error)

            if(sql.isAttrBool(attribute)):
                # this type of attribute cannot have a value
                error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(41).replace("-attr", attribute), 'type': "syntax"} #change from endAttr
                self.syntaxErrors.append(error)
                                            
                # check for unique id
                if (attribute.lower() == "id"):
                    for idVal in ids:
                        if(idVal.lower()==value): 
                            # error for duplicate id
                            error = {'line': line, 'column': offset, 'message' : attributeVal + sql.getErrMsg(41), 'type': "semantic"} #change from endAttr
                            self.semanticErrors.append(error)
                        else:
                            ids.append(attributeVal)

        # Check if tag and tag before tag are br tag
        if(prevTag.lower()=="br" and tag.lower()=="br"):
            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(37), 'type': "semantic"}
            self.semanticErrors.append(error)

        if(tag.lower() == "link" and (not styleHasRel or not styleHasType)):
            error = {'line': line, 'column': offset, 'message' : "This link tag does not have rel and/or type attributes. Make sure it looks like <link href='style.css' rel='stylesheet' type='text/css' />", 'type': "syntax"}
            self.syntaxErrors.append(error)

        if(tag.lower() == "script" and (not scriptHasType)):
            error = {'line': line, 'column': offset, 'message' : "Make sure you specify the type of your script by adding the type attribute to this tag.", 'type': "syntax"}
            self.syntaxErrors.append(error)


    def handle_endtag(self, tag):
        #print "Encountered an end tag:", tag
        #print "Last opened tag was: ", self.openedTag[-1]

        sql = SqlFunctions();
        matchFound = False
        line, offset = self.getpos()

        requiredClosingTags = ["html", "head", "body", "!doctype", "title", "meta", "main", "base"]

        if (sql.isSelfClosing(tag.lower())):
            return 0
        
        #Look for tag. If tag isn't closed (no match is found), mark as error on tag.

        while (len(self.openedTag) > 0 and not matchFound):

            #selfClosing = sql.isSelfClosing(tag)
            #if (not selfClosing):

            _tag = self.openedTag[-1]
            
            if (_tag.tagName == tag.lower()):
                matchFound = True
                if(tag.lower() in requiredClosingTags):                                 
                    self.requiredTags.append(tag.lower())
                    if(tag.lower() == "main"):
                        error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(47)}
                        self.practiceErrors.append(error)
                    
                    #Check singular tags
                    if(tag.lower() in self.singularTags):
                        
                        if (tag.lower()=="!doctype"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(8), 'type': "semantic"}
                        elif (tag.lower()=="html"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(9), 'type': "semantic"}
                        elif (tag.lower()=="head"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(10), 'type': "semantic"}
                        elif (tag.lower()=="title"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(11), 'type': "semantic"}
                        elif (tag.lower()=="body"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(16), 'type': "semantic"}
                        elif (tag.lower()=="main"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(46), 'type': "semantic"}
                        elif (tag.lower()=="base"):
                            error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(45), 'type': "semantic"}
                        
                        self.semanticErrors.append(error)
                    else:
                        self.singularTags.append(tag.lower())

                # Error messages for values that are not deprecated, but best practice asks they not be used
                if(tag.lower() == "s"):
                    error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(24), 'type': "practice"}
                    self.practiceErrors.append(error)
                
                if(tag.lower() == "i"):
                    error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(25), 'type': "practice"}
                    self.practiceErrors.append(error)

                if(tag.lower() == "b"):
                    error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(26), 'type': "practice"}
                    self.practiceErrors.append(error)
                
                if(tag.lower() == "u"):
                    error = {'line': line, 'column': offset, 'message' : sql.getErrMsg(27), 'type': "practice"}
                    self.practiceErrors.append(error)

            else:
                error = {'line': _tag.position[0], 'column': _tag.position[1], 'column_end': offset, 'message' : sql.getErrMsg(55).replace("--element", tag), 'type': "syntax"}
                self.syntaxErrors.append(error)
                # matchFound = True

            # if(sql.isDeprecated(tag)):
            #     error = {'line': _tag.position[0], 'column': _tag.position[1], 'column_end': offset, 'message' : sql.getErrMsg(29).replace("--element", tag), 'type': "deprecated"}
            #     self.deprecatedErrors.append(error)


            # If it is not a valid tag
            if(not sql.checkValidTag(tag)): 
                if(tag.lower() == "!doctype"):
                    self.requiredTags.append(tag)
                elif (tag.lower() == "doctype"):
                    error = {'line': _tag.position[0], 'column': _tag.position[1], 'column_end': offset, 'message' : sql.getErrMsg(2), 'type': "syntax"}
                    self.syntaxErrors.append(error)
                else:
                    error = {'line': _tag.position[0], 'column': _tag.position[1], 'column_end': offset, 'message' : sql.getErrMsg(18).replace("--tag",tag), 'type': "syntax"}
                    self.syntaxErrors.append(error)
                        
            # If it a deprecated tag
            if(sql.isDeprecated(tag)):
                error = {'line': _tag.position[0], 'column': _tag.position[1], 'column_end': offset, 'message' : sql.getErrMsg(29).replace("--element", tag), 'type': "deprecated"}
                self.deprecatedErrors.append(error)

            del self.openedTag[-1]

    def handle_data(self, data):

        if (len(self.openedTag) > 0):
            _tag = self.openedTag[-1]
            if (_tag.tagName.lower() == "script"):
                error = {'line': _tag.position[0], 'column': _tag.position[1], 'message' : "You shouldn't use inline JavaScript code, use a separate JavaScript file instead.", 'type': "practice"}
                self.practiceErrors.append(error)


        return 0
        # print "Encountered some data  :", data

    def parseEncapsulationErrors(self,errors):
        sql = SqlFunctions();

        for error in errors:
            errorCode = error.error
            line = error.line
            col = error.colStart
            colEnd = error.colEnd
            errorExcerpt = error.name
            if (errorExcerpt == None):
                errorExcerpt = ""

            message = sql.getErrMsg(errorCode);
            if (message == ""):
                    message = "No message could be found for error code: "+str(errorCode)
                    
            error = {'line': line, 'column': col, 'message': message, 'type': "syntax"}
            self.syntaxErrors.append(error)



    def parse(self, htmlString):

        sql = SqlFunctions();
        
        self.feed(htmlString)

        # final checks
        if(not self.hasDoctype):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(3), 'type': "syntax"}
            self.syntaxErrors.append(error)

        if(self.doctypeCount > 1):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(8), 'type': "syntax"}
            self.syntaxErrors.append(error)


        # Add any errors for required tags not being present
        if("html" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(4), 'type': "syntax"}
            self.syntaxErrors.append(error)

        if("head" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(5), 'type': "syntax"}
            self.syntaxErrors.append(error)
            
        if("body" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(7), 'type': "syntax"}
            self.syntaxErrors.append(error)

        if("title" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(6), 'type': "semantic"}
            self.semanticErrors.append(error)

        if("meta" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(32), 'type': "semantic"}
            self.semanticErrors.append(error)

                    
