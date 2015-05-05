from sql import SqlFunctions
from collections import deque
import copy # need copy so there's not just the 1 reference...

class Encapsulation:
    def __init__(self):
        self.ENCAPSULATION_ERROR = 48 # issues original 48
        self.ELEMENT_INSIDE_ITSELF = 49
        self.TABLE_ELEMENT_OUT_OF_TABLE = 50
        self.FORM_ELEMENT_OUT_OF_FORM = 51
        self.OUTSIDE_HTML_TAGS = 52
        self.INVALID_HEAD_ELEMENT = 53
        self.INVALID_BODY_ELEMENT = 54
        self.UNCLOSED_ELEMENT = 55
        self.STRAY_CLOSE_TAG = 56
        self.TABLE_ELEMENT_INCORRECT_ORDER = 57
        self.DUPLICATE_SINGULAR_TABLE_ELEMENT = 58
        self.NOT_IN_VALID_TABLE_ELEMENT = 59

        self.specialLoopsCount = 0

    # Flags to check whether certain elements have been opened.
        self.htmlElementOpen = False
        self.headElementOpen = False
        self.bodyElementOpen = False
        self.tableElementOpen = False
        self.formElementOpen = False
        self.innerTableElementOpen = False

        self.sql = SqlFunctions()

    	self.openedElements = deque()
    	self.tableElements = deque()
    	self.errorList = list()
    	self.encapErrorList = list()

    def getErrorList(self):

        errors = list()
        self.addUnclosedElements()
        self.addEncapErrorsToList()

        for error in self.errorList:
            if(not error in errors):
                errors.append(error)

        
        return errors
    
    def addUnclosedElements(self):
        while(len(self.openedElements) > 0):
            element = self.openedElements.pop()
            self.addError(element, self.UNCLOSED_ELEMENT)

    def addEncapErrorsToList(self):
        equality = False
        for encapError in self.encapErrorList:
            if(encapError.error == 9999): # changing from 0, how does anything get to here with error 9999
                encapError.error = self.ENCAPSULATION_ERROR # self.ENCAPSULATION_ERROR
            for error in self.errorList:
                if(encapError == error): 
                    equality = True;
                    break;

            if(not equality):
                self.errorList.append(encapError)

    def addError(self, element, errorCode):
        element.error = errorCode
    	self.errorList.append(element)
    
    def addEncapError(self, element, errorCode): # Simon This might  also be stuffing up.
        alreadyExists = False
        element.error = errorCode # change from errorCode ! change back!!!
        # self.errorList.append(element)
        for encapError in self.encapErrorList:
            if(self.compareElements(element, encapError)):
                alreadyExists = True
                break
            # if(element == encapError):
            #    alreadyExists = True
            #    break
        
        if(not alreadyExists):
            # secondNewError = element
            # secondNewError.error = 100023
            self.encapErrorList.append(element)

    def compareElements(self, element1, element2):
        check = False
        if(element1.name.lower() == element2.name.lower()):
            if(element1.line == element2.line):
                if(element1.colStart == element2.colStart):
                    if(element1.colEnd == element2.colEnd):
                        if(element1.error == element2.error):
                            check = True

    def encapElement(self, element, line, colStart, colEnd):
        e = Element(element, line, colStart, colEnd)
        cleanName = e.name
        if(e.name[0] == '/'):
            cleanName = e.name[1:]
        
        # Checks if a tag is added outside of the <html> tags. 
        if(not self.htmlElementOpen):
            if(not e.name.lower()=="html"):
                self.addError(e, self.OUTSIDE_HTML_TAGS)

        # Checks if a tag that cannot exist inside a <head> tag is added while
        # the <head> tag is open. 
        if(self.headElementOpen):
            if(e.name.lower()=="/head"):
                debugError = Element("test", 1, 2, 3)
                debugError.error = "Closing head tag..."
                # self.errorList.append(debugError)
            elif(not(self.sql.isMeta(cleanName) or cleanName.lower()=="title") 
                or e.name.lower()=="/head"):
                self.addError(e, self.INVALID_HEAD_ELEMENT)
                debugError = Element("test", 1, 2, 3)
                debugError.error = "Invalid element inside the head tag... tag(" + e.name.lower() + ")"
                # self.errorList.append(debugError)
        
        # Series of checks on tags when the <body> tag is open. 
        if(self.bodyElementOpen):
            # Checks if a table element is added outside of a table.
            if(self.sql.isTableElement(cleanName) and not self.tableElementOpen and 
                not self.innerTableElementOpen):
                self.addError(e, self.TABLE_ELEMENT_OUT_OF_TABLE);
                    
                # If the table element is a container for other table elements,
                # set the table container variable on.
                if(self.sql.isTableContainer(e.name)):
                        self.innerTableElementOpen = True;
            
            # Adds the table element to the table elements deque if valid. 
            if(self.sql.isTableElement(e.name) and self.tableElementOpen):
                self.tableElements.push(e.name)
                    
                # Detects if a singular table element being added already
                # exists within the currently open table. 
                if(self.sql.isTableSingular(e.name) 
                                and e.name in self.tableElements):
                    self.addError(e, self.DUPLICATE_SINGULAR_TABLE_ELEMENT)
            
            # Checks if a form element is being added outside of a form. 
            if(self.sql.isFormElement(cleanName) and not self.formElementOpen):
                self.addError(e, self.FORM_ELEMENT_OUT_OF_FORM)

        # If the tag is self-closing, it is not parsed into the encapsulation
        # function, as tag encapsulation is only relevant to elements with
        # start and end tags. 
        if(not self.sql.isSelfClosing(cleanName)):
            self.encapTag(e)

    def encapTag(self, e):
        elements = deque()
        
        # Checks if the tag given is a start tag.
        if(e.name[0] != '/'):
                
            # Used for form checks. 
            colgroupOpen = False
            trOpen = False

            # Used for li/ul nest checks. 
            noAdd = False
                
            # Iterates through the opened elements deque. 
            for element in self.openedElements:
                validNest = ""
                if(e.name.lower()=="li"):
                    validNest = "ul"
                if(e.name.lower()=="ul"):
                    validNest = "li"
                    
                # If a ul/li tag was added and a li/ul tag exists in the 
                # opened elements, the no add variable is flicked.
                if(element.name.lower()==validNest): # TODO: Simon .lower()?
                    noAdd = True
        
                # Checks that an element has not been opened inside another
                # element of the same type, with the exception of <div>,
                # <span> and <fieldset>. It also checks for <li>/<ul> nesting.
                if(e.name.lower()==element.name.lower()): # TODO: Simon .lower()?
                    if((not e.name.lower()=="div") 
                        or (e.name.lower()=="span")
                        or (e.name.lower()=="fieldset")):
                        if(not noAdd):
                            self.addError(e, self.ELEMENT_INSIDE_ITSELF)
                
                # Checks if a <colgroup> or <tr> tag has been opened. */
                if(element.name.lower()=="colgroup"):
                    colgroupOpen = True
                
                if(element.name.lower()=="tr"):
                    trOpen = True
                    
            # Various table element error checks.
            if(e.name.lower()=="caption" and (len(self.tableElements)>0)):
                self.addError(e, self.TABLE_ELEMENT_INCORRECT_ORDER)
            
            if(e.name.lower()=="col" and not colgroupOpen):
                self.addError(e, self.NOT_IN_VALID_TABLE_ELEMENT)
            
            if((e.name.lower()=="td" or e.name.lower()=="th") 
                and not trOpen):
                self.addError(e, self.NOT_IN_VALID_TABLE_ELEMENT)
            
            # Adds the tag to the opened elements deque.
            debugError = Element("test", 1, 2, 3)
            debugError.error = "Adding this tag to the opened wtf elements list...: " + e.name+ " line: " + str(e.line)
            # self.errorList.append(debugError)
            self.openedElements.append(e) # silly jono used appendleft here
            
            # Turns various boolean opened tag variables on. 
            if(e.name.lower()=="html"):
                self.htmlElementOpen = True
            
            if(e.name.lower()=="head"):
                self.headElementOpen = True
            
            if(e.name.lower()=="body"):
                self.bodyElementOpen = True
            
            if(e.name.lower()=="form"):
                self.formElementOpen = True
            
            if(e.name.lower()=="table"):
                self.tableElementOpen = True
                # Creates a new table deque if a <table> tag is detected. */
                self.tableElements = deque()
            
        # If the tag is an end tag.     
        else:
            self.specialLoopsCount = self.specialLoopsCount + 1
            debugError = Element("test", 1, 2, 3)
            debugError.error = "Loop number(" + str(self.specialLoopsCount) + ") for element(" + e.name + ") on line(" + str(e.line) + ")"
            # self.errorList.append(debugError)
            # debugError.error = "HEY BABY, THIS IS EDITING THE ERROR EVEN AFTER IT'S BEEN ADDED TO A LIST"
            
            # Add an error if an end tag is added without having a start tag. 
            if(len(self.openedElements) == 0):
                self.addEncapError(e, self.STRAY_CLOSE_TAG)

            for openEl in self.openedElements:
                debugError = Element("test", 1, 2, 3)
                debugError.error = "!!!Checking contents of openedElements. Name: " + openEl.name + " line(" + str(openEl.line) + ")"
                # self.errorList.append(debugError)

            subLoops = 0
                    
            while(len(self.openedElements)>0):
                # Checks if the close tag added is equal to the last element
                # in the opened elements deque, and removes it. Any opened tags
                # which have been popped off while checking for the appropriate
                # opening tag are readded to the opened elements deque. */
                openElement = self.openedElements.pop()
                self.openedElements.append(openElement)

                miniLoops = 0

                for openEl in self.openedElements:
                    miniLoops = miniLoops + 1
                    debugError = Element("test", 1, 2, 3)
                    debugError.error = "###Checking contents of openedElements. Miniloop(" + str(miniLoops) + ") Name: " + openEl.name + " line(" + str(openEl.line) + ")"
                    # self.errorList.append(debugError)

                subLoops = subLoops + 1
                
                debugError = Element("test", 1, 2, 3)
                debugError.error = "Made it inside the while statement mainloop(" + str(self.specialLoopsCount) + ") subloop(" + str(subLoops) + ") " + e.name.lower()[1:] + " " + openElement.name + " line: " + str(e.line)
                # self.errorList.append(debugError)

                hasThisClosed = False
            
                if(e.name.lower()[1:]==openElement.name): # why isn't this if statement passing?

                    hasThisClosed = True

                    debugError = Element("test", 1, 2, 3)
                    debugError.error = "The last two were a match on loop(" + str(self.specialLoopsCount) + "), lets remove: " + openElement.name + " from line(" + str(openElement.line) + ")"
                    # self.errorList.append(debugError)
                    
                    self.openedElements.pop()
                    self.reAddOpenedElements(elements)

                    for openEl in self.openedElements:
                        debugError = Element("test", 1, 2, 3)
                        debugError.error = "@@@Checking contents of openedElements. Name: " + openEl.name + " line(" + str(openEl.line) + ")"
                        # self.errorList.append(debugError)
                    
                    # Closes the opened tag variables if the end tag is detected.
                    if(e.name.lower()=="/html"):
                        self.htmlElementOpen = False
                            
                    if(e.name.lower()=="/head"):
                        self.headElementOpen = False
                        debugError = Element("test", 1, 2, 3)
                        debugError.error = "Closing the <head> tag!"
                        # self.errorList.append(debugError)
                            
                    if(e.name.lower()=="/body"):
                        self.bodyElementOpen = False
                    
                    # Closes the table opened variable, provided no other table
                    # has been opened. 
                    if(e.name.lower()=="/table"):
                        self.tableElementOpen = False
                        for openE in self.openedElements:
                            if(openE.name.lower()=="table"):
                                self.tableElementOpen = True
                    
                    # Closes the form opened variable, provided no other form
                    # has been opened. 
                    if(e.name.lower()=="/form"):
                        self.formElementOpen = False
                        for openE in self.openedElements:
                            if(openE.name.lower()=="form"):
                                self.formElementOpen = True
                    
                    # If a table container element is open, it closes the
                    # check variable only if an appropriate close tag is
                    # detected. */
                    if(self.innerTableElementOpen):
                        cleanName = e.name[1:]
                        if(self.sql.isTableContainer(cleanName)):
                            self.innerTableElementOpen = False
                    
                    break
                else:
                    # If the close tag does not match the last opened tag,
                    # add an error for that opened tag and remove it from the
                    # opened tags deque and add it to the temporary holding
                    # deque.

                    if(hasThisClosed):
                        debugError = Element("test", 1, 2, 3)
                        debugError.error = "!@!This stupid thing was closed.. and it's subloop(" + str(subLoops) + ") ...: " + ele.name+ " line: " + str(ele.line)
                        # self.errorList.append(debugError)
                    
                    ele = self.openedElements.pop()
                    self.addEncapError(ele, self.UNCLOSED_ELEMENT)
                    debugError = Element("test", 1, 2, 3)
                    debugError.error = "This tag hasn't been closed (" + str(hasThisClosed) + ") and it's subloop(" + str(subLoops) + ") ...: " + ele.name+ " line: " + str(ele.line)
                    # self.errorList.append(debugError)
                    newEle = Element(ele.name, ele.line, ele.colStart, ele.colEnd)
                    newEle.error = ele.error
                    elements.appendleft(newEle) #changed ele to newEle

        
            # If a close tag does not have a matching open tag within the
            # opened tag deque, add a stray close tag error on the close tag.
            if(len(self.openedElements)==0 and len(elements)>0):
                size = len(elements)
                debugError = Element("test", 1, 2, 3)
                debugError.error = "ABOUT TO RUN READDOPENED ELEMENTS due to " + e.name
                # self.errorList.append(debugError)
                self.reAddOpenedElements(elements)
                self.removeEncapErrors(size)
                self.addEncapError(e, self.STRAY_CLOSE_TAG)

    def reAddOpenedElements(self, elements):
        while(len(elements)>0):
                e = elements.pop()
                e.error = 9999 #changed from 9999
                self.openedElements.appendleft(e)

    def removeEncapErrors(self, number):
        for i in range(number):
                self.encapErrorList.pop()


class Element:
    def __init__(self, name, line, colStart, colEnd):
        self.name = name
        self.line = line
        self.colStart = colStart
        self.colEnd = colEnd
        self.error = 20001 # changing to 20001 from 0

    def getPosition(self):
        position = list()
        position.append(line)
        position.append(col)
                
        return position
