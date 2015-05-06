from sql import SqlFunctions
from encapsulation import Encapsulation
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        
        HTMLParser.__init__(self)

        # The main lists of errors for the entire file
        self.syntaxErrors = list()
        self.semanticErrors = list()
        self.deprecatedErrors = list()
        self.practiceErrors = list()

        # The class attributes

        self.openStyle = False       # True if a style tag is currently open 
        self.openScript = False      # True if a script tag is currently open
        self.openSVG = False         # True if an SVG tag is currently open
        self.openMath = False        # True if a math tag is currently open
        self.openCode = False        # True if a code tag is currently open
        self.endEscapedTagPhase = 0  # A value to keep track of parsing the above "escape" tags
        self.openDoctype = False     # True if the doctype has been opened
        self.openTag = False         # True if a tag has been opened
        self.closeTag = False        # True if a tag has been closed
        self.openAttr = False        # True if an attribute is currently open
        self.startComment = False    # True if a comment is currently open
        self.startPHP = False        # True if a ?php tag is currently open
        self.tag = ""                # The name of the current tag in parsing
        self.endTagName = False      # True if the end of the tag name has been read
        self.tagChecked = False      # True if the tag ha sbeen checked
        self.faultyTag = False
        self.singularTags = list()
        self.requiredTags = list()
        self.isClosingTag = False
        self.whiteSpaceFlag = False

        self.openedTag = list()
        self.closedTag = list()

    def closeTheTag(self):
        self.openDoctype = False
        self.closeTag = True
        self.openTag = False
        self.tag = ""
        self.endTagName = False
        self.tagChecked = False
        self.faultyTag = False

    # Andy's stuff

    def handle_starttag(self, tag, attributes):

        sql = SqlFunctions();

        # print "Encountered a start tag:", tag
        self.openedTag.append(tag);

        # Check attributes

        attrList = sql.getAttr(tag.lower())
        
        for attribute, value in attributes:

            validAttr = True if attribute in attrList else False
                                              
            if (attribute[0:5].lower() == "data-"):
                validAttr = True
                    
            if (not validAttr):
                error = {'line': 1, 'column': 1, 'message' : attribute + " " + sql.getErrMsg(22), 'type': tag}
                self.syntaxErrors.append(error)
                debugError = {'line': 1, 'column': 1, 'message' : "Not a valid attribute("+attribute+")", 'type': "practice"}
                self.practiceErrors.append(debugError) 
            elif (sql.isDeprecatedAttribute(attribute)):
                error = {'line': 1, 'column': 1, 'message' : sql.getErrMsg(30).replace("--attr",attribute).replace("--tag",tag), 'type': "deprecated"}
                self.deprecatedErrors.append(error) 


    def handle_endtag(self, tag):
        #print "Encountered an end tag:", tag
        #print "Last opened tag was: ", self.openedTag[-1]

        matchFound = False

        #Look for tag. If tag isn't closed (no match is found), mark as error on tag.

        while (len(self.openedTag) > 0 and not matchFound):

            if (self.openedTag[-1] == tag.lower()):
                if(tag.lower() in ["html", "head", "body", "!doctype", "title", "meta", "main", "base"]):                                 
                    self.requiredTags.append(tag.lower())
                matchFound = True
            else:
                error = {'line': 1, 'column': 0, 'message' : self.openedTag[-1] + ' not closed...', 'type': "syntax"}
                self.syntaxErrors.append(error)
                # matchFound = True
        
            del self.openedTag[-1]

    def handle_data(self, data):
        return 0
        # print "Encountered some data  :", data


    # End of Andy's stuff


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
        
        self.feed(htmlString)

        prevTag = ""
        tagStartSet = False
        # Instantiate the sqlFunctions class
        sql = SqlFunctions()
        # Instantiate the encapsulation class
        encap = Encapsulation()

        attrPhase = 0
        # Iterates over the lines of the given file
        for lineNum, lineString in enumerate(htmlString.splitlines()):

            debugError = {'line': 1, 'column': 1, 'message' : "Looping for each line("+str(lineNum)+")", 'type': "practice"}
            # self.practiceErrors.append(debugError)
            
            # Check for open tags
            for colOffset, char in enumerate(lineString):
                # ==============================================
                # check whether one of the ignored tags is open,
                # in which case content will be unchecked
                # until the associated end tag  is found
                # ==============================================
                if (self.openStyle or self.openScript or self.openSVG or self.openMath or self.openCode):

                        if (self.endEscapedTagPhase == 0):
                            if (char == '<'):
                                # look for next char
                                self.endEscapedTagPhase = 1

                        elif (self.endEscapedTagPhase == 1): 
                                if (char == '/') :
                                        # look for next char
                                        self.tagStart = colOffset
                                        self.endEscapedTagPhase = 2
                                elif (char != ' '): 
                                        # reset tag
                                        self.endEscapedTagPhase = 0

                        elif (self.endEscapedTagPhase == 2):
                                if ((char.lower() == 's' and (self.openStyle or self.openScript or openSVG))
                                        or(char.lower() == 'm' and self.openMath)
                                        or(char.lower() == 'c' and self.openCode)):
                                        # look for next char
                                        self.endEscapedTagPhase = 3
                                elif (char != ' '):
                                        # reset tag
                                        self.endEscapedTagPhase = 0
                                
                        elif (self.endEscapedTagPhase == 3):
                                if ((char.lower() == 't' and self.openStyle)
                                        or (char.lower() == 'c' and self.openScript)
                                        or (char.lower() == 'v' and self.openSVG)
                                        or (char.lower() == 'a' and self.openMath)
                                        or (char.lower() == 'o' and self.openCode)):
                                        # look for next char
                                        self.endEscapedTagPhase = 4
                                else:
                                        # reset tag
                                        self.endEscapedTagPhase = 0

                        elif (self.endEscapedTagPhase == 4):
                                if ((char.lower() == 'y' and self.openStyle)
                                        or (char.lower() == 'r' and self.openScript)
                                        or (char.lower() == 't' and self.openMath)
                                        or (char.lower() == 'd' and self.openCode)):
                                        # look for next char
                                        self.endEscapedTagPhase = 5
                                elif(char.lower() == 'g' and self.openSVG):
                                        self.endTagColumnNo = j
                                        self.endEscapedTagPhase = 8
                                        ignore = "SVG"
                                else:
                                        # reset tag
                                        self.endEscapedTagPhase = 0
                                
                        elif (self.endEscapedTagPhase == 5): 
                                if ((char.lower() == 'l' and self.openStyle)
                                        or (char.lower() == 'i' and self.openScript)):
                                        # look for next char
                                        self.endEscapedTagPhase = 6
                                elif((char.lower() == 'h' and self.openMath)):
                                        self.endTagColumnNo = colOffset
                                        self.endEscapedTagPhase = 8
                                        ignore = "MATH"
                                elif(char.lower() == 'e' and self.openCode):
                                        self.endTagColumnNo = colOffset
                                        self.endEscapedTagPhase = 8
                                        ignore = "CODE"
                                else:
                                        # reset tag
                                        self.endEscapedTagPhase = 0
                                        
                        elif (self.endEscapedTagPhase == 6):
                                if ((char.lower() == 'p' and self.openScript)):
                                        # look for next char
                                        self.endEscapedTagPhase = 7
                                elif(char.lower() == 'e' and self.openStyle):
                                        self.endTagColumnNo = colOffset
                                        self.endEscapedTagPhase = 8
                                        ignore = "STYLE"
                                else:
                                        # reset tag
                                        self.endEscapedTagPhase = 0

                        elif (endEscapedTagPhase == 7):
                                if (char.lower() == 't' and self.openScript):
                                        # look for next char
                                        self.endEscapedTagPhase = 8
                                        self.endTagColumnNo = colOffset
                                        ignore = "SCRIPT"
                                else:
                                        # reset tag
                                        self.endEscapedTagPhase = 0
                        
                        elif (self.endEscapedTagPhase == 8):
                                if (char == '>'):
                                        # tag has been closed
                                        self.endEscapedTagPhase = 0
                                        
                                        if(ignore=="SVG"):
                                                self.openSVG = False
                                                encap.encapElement("/svg", lineNum+1, self.tagStart, self.endTagColumnNo);
                                        elif(ignore=="MATH"):
                                                self.openMath = False
                                                encap.encapElement("/math", lineNum+1, self.tagStart, self.endTagColumnNo);
                                        elif(ignore=="CODE"):
                                                self.openCode = False
                                                encap.encapElement("/code", lineNum+1, self.tagStart, self.endTagColumnNo);
                                        elif(ignore=="STYLE"):
                                                self.openStyle = False
                                                encap.encapElement("/style", lineNum+1, self.tagStart, self.endTagColumnNo);
                                        elif(ignore=="SCRIPT"):
                                                self.openScript = False
                                                encap.encapElement("/script", lineNum+1, self.tagStart, self.endTagColumnNo);
                                                
                                elif (char != ' '):
                                        # reset tag
                                        self.endEscapedTagPhase = 0
                                
                        continue
            

                # ==============================================
                # Doctype fix start
                # ==============================================
                if(self.openDoctype):
                    if(attrPhase == 1):
                        if(char == ' '):
                            continue
                        if(char.lower() == 'h'):
                            attrPhase = 2
                            continue
                        else:
                            error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(1), 'type': "syntax"}
                            self.syntaxErrors.append(error)
                            attrPhase = 5
                            if(char == '>'):
                                self.closeTheTag()
                            continue
                                
                    if (attrPhase == 2):
                        if (char.lower() == 't'):
                            attrPhase = 3
                            continue
                        else:
                            error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(1), 'type': "syntax"}
                            self.syntaxErrors.append(error)
                            attrPhase = 5
                            if (char == '>'):
                                self.closeTheTag()
                            continue

                    if (attrPhase == 3):
                        if (char.lower() == 'm'):
                            attrPhase = 4
                            continue
                        else:
                            error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(1), 'type': "syntax"}
                            self.syntaxErrors.append(error)
                            attrPhase = 5
                            if (char == '>'):
                                self.closeTheTag()
                            continue
                                
                    if (attrPhase == 4):
                        if (char.lower() == 'l'):
                            attrPhase = 5
                            continue
                        else:
                            error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(1), 'type': "syntax"}
                            self.syntaxErrors.append(error)
                            attrPhase = 5
                            if (char == '>'):
                                self.closeTheTag()
                            continue
                        
                    
                    if (attrPhase == 5):
                            if (char == '>'):
                                self.closeTheTag()
                            elif (char != ' '):
                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(1), 'type': "syntax"}
                                self.syntaxErrors.append(error)
                                attrPhase = 6
                            continue
                    
                    if (attrPhase == 6):
                            if (char == '>'):
                                self.closeTheTag()
                            continue

                # ==============================================
                # Doctype fix end
                # ==============================================

                # ==============================================
                # Attribute checking start
                # ==============================================
                if (self.openAttr):
                        if (attrPhase == 1):
                                # Retrieve the list of valid Attributes from the database for this tag
                                attrList = sql.getAttr(tag)
                                validAttr = False

                                debugError = {'line': 1, 'column': 1, 'message' : "Just got the list of attributes attrlistLength("+str(len(attrList))+")", 'type': "practice"}
                                self.practiceErrors.append(debugError)
                               
                                # looking for end of attribute key
                                if (char == ' '):
                                        # attribute key has ended
                                        attribute = lineString[attrStart:colOffset]
                                        debugError = {'line': 1, 'column': 1, 'message' : "Checking attribute("+attribute+")", 'type': "practice"}
                                        self.practiceErrors.append(debugError)
                                        endAttrColumnNo = colOffset - 1
                                        if(attribute.lower() in attributeList):
                                            # Duplicate attribute use for this tag
                                            error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + sql.getErrMsg(44), 'type': "syntax"}
                                            self.syntaxErrors.append(error)          
                                        else:
                                            attributeList.append(attribute.lower())
                                        
                                        
                                        if (tag.lower() =="meta" and attribute.lower() == "charset"):
                                            self.requiredTags.append(tag.lower())

                                        validAttr = True if attribute in attrList else False
                                              
                                        if (attribute[0:5].lower() == "data-"):
                                            validAttr = True
                                                
                                        if (not validAttr):
                                            error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + " " + sql.getErrMsg(22), 'type': tag}
                                            self.syntaxErrors.append(error)
                                            debugError = {'line': 1, 'column': 1, 'message' : "Not a valid attribute("+attribute+")", 'type': "practice"}
                                            self.practiceErrors.append(debugError)
                                                
                                        elif (sql.isDeprecatedAttribute(attribute, tag)):
                                            error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(30).replace("--attr",attribute).replace("--tag",tag), 'type': "deprecated"}
                                            self.deprecatedErrors.append(error)   
                                        
                                        attrPhase = 2
                                        
                                elif (char == '>' or char == '/'):
                                        # did not find value for attribute
                                        attribute = lineString[attrStart:colOffset]
                                        endAttrColumnNo = colOffset-1
                                        if(not sql.isAttrBool(attribute)):
                                                # did not find a value for the key
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(43).replace("-attr", attribute), 'type': "syntax"}
                                                self.syntaxErrors.append(error)   
                                        
                                        if(attribute.lower() in attributeList):
                                                # Duplicate attribute use for this tag
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + sql.getErrMsg(44), 'type': "syntax"}
                                                self.syntaxErrors.append(error)     
                                        else:
                                                attributeList.append(attribute.lower())
                                           
                                        validAttr = True if attribute in attrList else False

                                        if (attribute[0:5].lower() == "data-"):
                                            validAttr = True
                                                        
                                        
                                        if (not validAttr):
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + " " + sql.getErrMsg(22), 'type': tag}
                                                self.syntaxErrors.append(error)
                                                debugError = {'line': 1, 'column': 1, 'message' : "Not a valid (no value either?) attribute("+attribute+")", 'type': "practice"}
                                                self.practiceErrors.append(debugError)
                                                
                                        elif (sql.isDeprecatedAttribute(attribute, tag)):
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(30).replace("--attr",attribute).replace("--tag",tag), 'type': "deprecated"}
                                                self.deprecatedErrors.append(error)   

                                        attrPhase = 0
                                        self.openAttr = False
                                        attribute = ""
                                        continue
                                
                                elif (char == '='): 
                                        # attribute key has ended
                                        attribute = lineString[attrStart:colOffset]
                                        endAttrColumnNo = colOffset-1
                                        if(attribute.lower() in attributeList):
                                                # Duplicate attribute use for this tag
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + sql.getErrMsg(44), 'type': "syntax"}
                                                self.syntaxErrors.append(error)  
                                        else:
                                                attributeList.append(attribute.lower())
                                        
                                        if (tag.lower() =="meta" and attribute.lower() == "charset"):
                                            self.requiredTags.append(tag.lower())
                                        
                                        validAttr = True if attribute in attrList else False

                                        for testAttribute in attrList:
                                            debugError = {'line': 1, 'column': 1, 'message' : "Attribute list("+testAttribute+")", 'type': "practice"}
                                            self.practiceErrors.append(debugError)
                                        
                                        if (attribute[0:5].lower() == "data-"):
                                            validAttr = True
                                                
                                        if (not validAttr):
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : attribute + " " + sql.getErrMsg(22), 'type': tag}
                                                self.syntaxErrors.append(error)   
                                                debugError = {'line': 1, 'column': 1, 'message' : "Nooot a valid (up to =) attribute("+attribute+") attrlistLength("+str(len(attrList))+")", 'type': "practice"}
                                                self.practiceErrors.append(debugError)
                                                
                                        elif (sql.isDeprecatedAttribute(attribute)):
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(30).replace("--attr",attribute).replace("--tag",tag), 'type': "deprecated"}
                                                self.deprecatedErrors.append(error)  
                                        
                                        attrPhase = 3
                                
                                continue
                                                         
                        elif (attrPhase == 2):
                                # looking for the end of whitespace before the =
                                if (char == ' '):
                                        continue
                                elif (char == '='):
                                        attrPhase = 3
                                        continue
                                else:
                                        if(not sql.isAttrBool(attribute)):
                                                 # did not find a value for the key
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(43).replace("-attr", attribute), 'type': "syntax"}
                                                self.syntaxErrors.append(error)  
                                        
                                        attrPhase = 0
                                        self.openAttr = False
                                        attribute = ""
                                
                        elif (attrPhase == 3):
                                # looking for quotes to start 
                                if (char == ' '):
                                    continue
                                elif (char == '"'):
                                        attrPhase = 4
                                        attrValStart = colOffset
                                elif (char == '\''):
                                        attrPhase = 5
                                        attrValStart = colOffset
                                elif (char == '#' and attribute.lower()=="href"):
                                        if (lineString[colOffset+1] == ' ' or lineString[colOffset+1] == '>' or lineString[colOffset+1] == '/'): 
                                                # unquoted # for href
                                                error = {'line': lineNum+1, 'column': colOffset, 'message' : sql.getErrMsg(42), 'type': "practice"}
                                                self.practiceErrors.append(error)  
                                                
                                                attrPhase = 0
                                                self.openAttr = False
                                                attribute = ""
                                        
                                        continue
                                else:
                                        # value not enclosed in quotes
                                        attrPhase = 6
                                        attrValStart = colOffset
                                
                                continue
                        elif (attrPhase == 4):
                                # looking for end of double quotes
                                if (char == '"'): 
                                
                                        if(sql.isAttrBool(attribute)):
                                                # this type of attribute cannot have a value
                                                error = {'line': lineNum+1, 'column': endAttrColumnNo, 'message' : sql.getErrMsg(41).replace("-attr", attribute), 'type': "syntax"} #change from endAttr
                                                self.syntaxErrors.append(error)
                                                
                                        # check for unique id
                                        if (attribute.lower() == "id"):
                                                attributeVal = lineString[attrValStart+1: colOffset-1]
                                                matchedID = False
                                                for idVal in ids:
                                                    if(idVal.lower()==attributeVal): 
                                                        matchedID = true
                                                
                                                if (matchedID):
                                                        # error for duplicate id
                                                        error = {'line': lineNum+1, 'column': endAttrColumnNo, 'message' : attributeVal + sql.getErrMsg(41), 'type': "semantic"} #change from endAttr
                                                        self.semanticErrors.append(error)
                                                else:
                                                        ids.append(attributeVal)
                                                
                                        # reset attribute flags
                                        attrPhase = 0
                                        self.openAttr = False
                                        attribute = ""
                                
                                continue
                            
                        elif (attrPhase == 5):
                                # looking for end of single quotes
                                if (char == '\''):
                                        
                                        if(sql.isAttrBool(attribute)):
                                                # this type of attribute cannot have a value
                                                error = {'line': lineNum+1, 'column': endAttrColumnNo, 'message' : sql.getErrMsg(41).replace("-attr", attribute), 'type': "syntax"} #changed from endAttr
                                                self.syntaxErrors.append(error)                               
                                        
                                        # check for unique id
                                        if (attribute.lower()=="id"):
                                                attributeVal = lineString[attrValStart+1: colOffser-1]
                                                matchedID = False
                                                for idVal in ids:
                                                    if(idVal.lower()==attributeVal): 
                                                        matchedID = true
                                                        
                                                if (matchedID):
                                                        # error for duplicate id
                                                        error = {'line': lineNum+1, 'column': endAttrColumnNo, 'message' : attributeVal + sql.getErrMsg(41), 'type': "semantic"} #changed from endAttr
                                                        self.semanticErrors.append(error)
                                                else: 
                                                        ids.append(attributeVal)
                                                
                                        # reset attribute flags
                                        attrPhase = 0
                                        self.openAttr = False
                                        attribute = ""
                                
                                continue
                        elif (attrPhase == 6): 
                                # looking for end of attribute
                                if (char == ' ' or char == '/' or char == '>'):
                                        attributeVal = lineString[attrValStart:colOffset]
                                        error = {'line': lineNum+1, 'column': endAttrColumnNo, 'message' : sql.getErrMsg(38).replace("-attval", attributeVal).replace("--attval", attributeVal).replace("--att", attribute), 'type': "semantic"} #changed from endAttr
                                        self.semanticErrors.append(error) 
                                        
                                        # reached end of attribute value
                                        attrPhase = 0
                                        self.openAttr = False
                                        attribute = ""
                                
                                continue
                        

                # ==============================================
                # Attribute checking end
                # ==============================================

                # ==============================================
                # Tag checking start
                # ==============================================
                if(char == '<'):
                    self.openTag = True
                    continue

                if(self.openTag and not tagStartSet):
                    if(char == ' '): 
                        continue
                        
                    tagStart = colOffset # Simon adding + 1 from java file
                    tagStartSet = True
                    # Check if opened a comment tag
                    if((char=='!') and (lineString[colOffset+1]=='-') and (lineString[colOffset+2]=='-')):
                        self.startComment = True
                        self.openTag = False
                            
                    # Check if opened a php tag
                    if((char=='?') and (lineString[colOffset+1].lower()=='p') and (lineString[colOffset+2].lower()=='h') and (lineString[colOffset+3].lower()=='p')):
                        self.startPHP = True

                # As long as a comment tag is not open, another tag is open and 
                # whitespace has not been reached to signal the end of the tag name:
                if(self.openTag and not self.startPHP and not self.startComment):
                        debugError = {'line': 1, 'column': 1, 'message' : "Open tag, nothing else open.", 'type': "practice"}
                        # self.practiceErrors.append(debugError)
                        if(not self.whiteSpaceFlag):
                                debugError = {'line': 1, 'column': 1, 'message' : "Not self.whiteSpaceFlag", 'type': "practice"}
                                # boop self.practiceErrors.append(debugError)
                                if(char==' ' or char=='>' or char=='\t'):
                                        debugError = {'line': 1, 'column': 1, 'message' : "Line:("+lineString+") Tag:("+lineString[tagStart:colOffset]+") tagStart("+str(tagStart)+") ColOffset("+str(colOffset)+") Made it into space, close or newline bit", 'type': "practice"}
                                        # self.practiceErrors.append(debugError)
                                        if((char==' ' or char=='\t') and self.endTagName): 
                                            self.whiteSpaceFlag=True
                                        
                                        if (self.openAttr == True): 
                                            self.openAttr = False

                                        if (lineString[tagStart:colOffset-1].strip()!="/" and len(lineString[tagStart:colOffset-1].strip()) > 0):
                                                debugError = {'line': 1, 'column': 1, 'message' : "Could reset Line:("+lineString+") except for the endTagName issue", 'type': "practice"}
                                                # self.practiceErrors.append(debugError)
                                        
                                        if (not self.endTagName and lineString[tagStart:colOffset].strip()!="/" and len(lineString[tagStart:colOffset].strip()) > 0):
                                                debugError = {'line': 1, 'column': 1, 'message' : "Line:("+lineString+") Resetting the tag!!!", 'type': "practice"}
                                                # self.practiceErrors.append(debugError)
                                                tag = lineString[tagStart:colOffset]
                                                tag = tag.strip().lower()
                                                self.requiredTags.append(tag)
                                                # Check all of the singular and required tags
                                                if(tag.lower() in ["html","head","body","!doctype","title","meta","main","base"]):                                 
                                                        self.requiredTags.append(tag.lower())
                                                        if(tag.lower() == "main"):
                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(47)}
                                                            self.practiceErrors.append(error)
                                                        
                                                        if(not tag.lower() == "meta"): 
                                                                if(tag.lower() in self.singularTags):
                                                                        if (tag.lower()=="!doctype"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(8), 'type': "semantic"}
                                                                        elif (tag.lower()=="html"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(9), 'type': "semantic"}
                                                                        elif (tag.lower()=="head"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(10), 'type': "semantic"}
                                                                        elif (tag.lower()=="title"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(11), 'type': "semantic"}
                                                                        elif (tag.lower()=="body"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(16), 'type': "semantic"}
                                                                        elif (tag.lower()=="main"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(46), 'type': "semantic"}
                                                                        elif (tag.lower()=="base"):
                                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(45), 'type': "semantic"}
                                                                        
                                                                        self.semanticErrors.append(error)
                                                                else:
                                                                        self.singularTags.append(tag.lower())
                                                  
                                               
                                                endTagColumnNo = colOffset-1
                                                tagStartSet =  False #problem is where tagStartSet is changed to false
                                                
                                                # Error messages for values that are not deprecated, but best practice asks they not be used
                                                if(tag.lower() == "s"):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(24), 'type': "practice"}
                                                    self.practiceErrors.append(error)
                                                
                                                if(tag.lower() == "i"):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(25), 'type': "practice"}
                                                    self.practiceErrors.append(error)

                                                if(tag.lower() == "b"):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(26), 'type': "practice"}
                                                    self.practiceErrors.append(error)
                                                
                                                if(tag.lower() == "u"):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(27), 'type': "practice"}
                                                    self.practiceErrors.append(error)
                                                
                                                attrPhase = 0
                                                openAttr = False
                                                
                                                # Initiate required attributes list
                                                attributeList = list()
                                                
                                                # Check if tag and tag before tag are br tag
                                                if(prevTag.lower()=="br" and tag.lower()=="br"):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(37), 'type': "semantic"}
                                                    self.semanticErrors.append(error)
                                                
                                                # Assign tag to prevTag
                                                prevTag = tag
                                                
                                                if(not tag.lower()=="!doctype"):
                                                        if (len(tag) > 0):
                                                                encap.encapElement(tag.lower(), lineNum+1, tagStart, endTagColumnNo)
                                                else:
                                                        openDoctype = True
                                                        attrPhase = 1
                                                            
                                                               
                                                if (len(tag) > 0):
                                                        debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : "Tag info(" + tag + ")", 'type': "semantic"}
                                                        # self.semanticErrors.append(debugError)
                                                        if (tag[0]=="/"):
                                                            debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : "HEY! This is a closing(" + tag[0] + ") tag:(" + tag + ")", 'type': "semantic"}
                                                            # self.semanticErrors.append(debugError)
                                                            self.isClosingTag = True
                                                            tag = tag[1:]
                                                        else:
                                                            self.isClosingTag = False
                                                        
                                                
                                                self.endTagName = True
                                                if (char==' ' or char=='\t'):
                                                    self.whiteSpaceFlag=True # missing this?
                                                    continue 
                                        
                                        if (not self.tagChecked and self.endTagName):

                                                # If it is not a valid tag
                                                if(not sql.checkValidTag(tag)): 
                                                        if(tag.lower() == "!doctype"):
                                                            self.requiredTags.append(tag)
                                                        elif (tag.lower() == "doctype"):
                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(2), 'type': "syntax"}
                                                            self.syntaxErrors.append(error)
                                                            self.faultyTag = True
                                                        else:
                                                            error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(18).replace("--tag",tag), 'type': "syntax"}
                                                            self.syntaxErrors.append(error)
                                                            self.faultyTag = True
                                                            
                                                # If it a deprecated tag
                                                elif(sql.isDeprecated(tag)):
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(29).replace("--element", tag), 'type': "deprecated"}
                                                    self.deprecatedErrors.append(error)
                                                    self.faultyTag = True
                                                
                                                self.tagChecked = True
                                        
                                        
                                
                                        if(char=='>'):
                                        
                                            attribute = ""
                                            self.openAttr = False
                                            attrPhase = 0
                                            
                                            if (not self.isClosingTag):
                                                # Get the list of required attributes for a tag from the database
                                                requiredAttributes = sql.requiresAttr(tag.lower())
                                                erroredAttrAlready = False
                                                for reqAttr in requiredAttributes: 
                                                        if(not reqAttr.lower() in attributeList): 
                                                                if(reqAttr.lower()=="alt"):
                                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(36), 'type': "practice"}
                                                                    self.practiceErrors.append(error)
                                                                    erroredAttrAlready = True
                                                                    
                                                                if(reqAttr.lower()=="name") and (tag.lower()=="input"):
                                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(35), 'type': "practice"}
                                                                    self.practiceErrors.append(error)
                                                                    erroredAttrAlready = True
                                                                    
                                                                if(reqAttr.lower()=="value") and (tag.lower()=="input"):
                                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(34), 'type': "practice"}
                                                                    self.practiceErrors.append(error)
                                                                    erroredAttrAlready = True
                                                                    
                                                                if(not erroredAttrAlready):
                                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(21).replace("--tag", tag).replace("--attr", reqAttr), 'type': "syntax"}
                                                                    self.syntaxErrors.append(error)

                                            # Check if self closing
                                            selfClosing = sql.isSelfClosing(tag)
                                            # Need to make this false for a final end tag...
                                            debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : "Line:("+lineString+") What is the endTagBoolean?("+str(self.isClosingTag)+")", 'type': "practice", 'debug': tag}
                                            # self.practiceErrors.append(debugError)

                                            # Move backwards from the detected '>' to see if the first value other than whitespace is a '/'
                                            closingChecker = colOffset-1
                                            while (lineString[closingChecker] == ' ' and closingChecker > 0):
                                                closingChecker = closingChecker - 1
                                                            

                                            # Check if comment tag closed
                                            if (selfClosing):
                                                debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : "Self closing tag:("+lineString+")", 'type': "practice", 'debug': tag} #original message: sql.getErrMsg(19).replace("--element_uc", tag)
                                                # self.practiceErrors.append(debugError)
                                                if(lineString[closingChecker] != '/'):
                                                    selfClosingError = True
                                                    # Simon: I've got a feeling things are getting...
                                                    debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(19).replace("--element_uc", tag), 'type': "practice", 'debug': tag} #original message: sql.getErrMsg(19).replace("--element_uc", tag)
                                                    # self.practiceErrors.append(debugError)
                                                    error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(19).replace("--element_uc", tag), 'type': "practice", 'debug': tag} #original message: sql.getErrMsg(19).replace("--element_uc", tag)
                                                    self.practiceErrors.append(error)
                                                else: 
                                                    selfClosingError = False
                                                    if (closingChecker > 0):
                                                        if (lineString[closingChecker-1] != ' '): 
                                                                selfClosingError = True
                                                                    
                                                    if (selfClosingError):
                                                        error = {'line': lineNum+1, 'column': closingChecker, 'message' : sql.getErrMsg(33), 'type': "practice"}
                                                        self.practiceErrors.append(error)
                                                selfClosing = False
                                            elif (not selfClosing):             
                                                if(lineString[closingChecker] == '/'): 
                                                    selfClosingError = True
                                                                
                                                    if (closingChecker > 0):
                                                        if (lineString[closingChecker-1] != ' '): 
                                                            selfClosingError = True
                                                                         
                                                    if (selfClosingError):
                                                        error = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : sql.getErrMsg(31).replace("--element_uc", tag), 'type': "semantic"}
                                                        self.semanticErrors.append(error)                                                            
                                                        
                                                selfClosing = False
                                                    
                                                    
                                            if(tag.lower() == "script"):
                                                self.openScript = True
                                                    
                                                    
                                            elif(tag.lower() == "style"): 
                                                self.openStyle = True
                                                    
                                                    
                                            elif(tag.lower() == "svg"):
                                                self.openSvg = True
                                                    
                                                    
                                            elif(tag.lower() == "math"):
                                                self.openMath = True
                                                    
                                                    
                                            elif(tag.lower() == "code"):
                                                self.openCode = True
                                    
                                            # Resets flag values and tag string 
                                            self.closeTheTag()
                                            tagStartSet = False # trying to see if setting tagStart to false works here
                                            debugError = {'line': lineNum+1, 'column': endTagColumnNo, 'message' : "Tagstart set to false for Line:(" + str(lineNum) + ") tag("+tag+") line("+lineString+") closingChecker("+str(closingChecker)+") excerpt("+lineString[closingChecker]+")", 'type': "practice", 'debug': tag} #original message: sql.getErrMsg(19).replace("--element_uc", tag)
                                            # self.practiceErrors.append(debugError)
                                
                        
                        
                        
                        # ==============================================
                        # Tag checking end
                        # ==============================================
                        
                        # Signal the end of the tag name and the beginning of an attribute
                        else:
                            debugError = {'line': 1, 'column': 1, 'message' : "End of tag name", 'type': "practice"}
                            self.practiceErrors.append(debugError)
                            if(tag != "!doctype"):
                                if (colOffset != 0): 
                                    if(char != '>'): 
                                        if (lineString[colOffset-1] == ' ') and (char != ' '):
                                            if(char.isalpha()): 
                                                attrStart = colOffset
                                                self.openAttr = True
                                                attrPhase = 1
                                                debugError = {'line': 1, 'column': 1, 'message' : "Just reached the end of the tag. Setting openAttr to true", 'type': "practice"}
                                                self.practiceErrors.append(debugError)

                                        elif(char ==' '):
                                            continue

                                self.whiteSpaceFlag = False
                                
                if (self.startComment == True and colOffset > 2): 
                    if(lineString[colOffset-2]=='-') and (lineString[colOffset-1]=='-') and (char=='>'):
                        self.closeTheTag()
                        attrPhase = 0
                        self.openAttr = False
                        self.startComment = False
                        continue
                        
                
                if(self.startPHP == True and colOffset > 1):
                    if(lineString[colOffset-1]=='?') and (char=='>'): 
                        self.closeTheTag()
                        attrPhase = 0
                        self.openAttr = False
                        self.startPHP = False
                        continue
                
                
                # If an attribute has been reached and finished via the = operator
                if(char == '='):
                    if(openAttr == True):
                        attrList = sql.getAttr(tag)
                        validAttr = False
                        for attr in attrList:
                            if(attr.lower() == attribute.lower()):
                                validAttr = True    

                        if (not validAttr):
                            error = {'line': lineNum+1, 'column': self.endTagColumnNo, 'message' : attr + " " + sql.getErrMsg(23), 'type': "syntax"}
                            self.syntaxErrors.append(error)
   
        # Grab the encapsulation errors for the file
        self.parseEncapsulationErrors(encap.getErrorList())
        
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

        if("!doctype" not in self.requiredTags):
            error = {'line': 1, 'column': 0, 'message' : sql.getErrMsg(3), 'type': "syntax"}
            self.syntaxErrors.append(error)

        if (len(self.openedTag) > 0):
            error = {'line': 1, 'column': 0, 'message' : 'some tags are not closed...', 'type': "syntax"}
            self.syntaxErrors.append(error)

                    
