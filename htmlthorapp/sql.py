from htmlthorapp.models import Error, Attribute, Element

class SqlFunctions:
    def __init__(self):
        self.begun = True
    
    def checkValidTag(self, tagName):
        try:
            tag = Element.objects.get(ename = tagName)
            if(tag.ename == tagName):
                return True
        except:
            return False
    
    # Returns the error message string for this error code
    def getErrMsg(self, errCode):
        try:
            return Error.objects.get(id=errCode).message
        except:
            return ""

    # Returns all attributes in a list for this tag
    def getAttr(self, tagName):
        try:
            attrList = list()
            for attr in Attribute.objects.filter(element = Element.objects.get(ename=tagName).id):
                attrList.append(attr.aname)
            return attrList
        except:
            return list()

    # Returns whether this attribute is a boolean one
    def isAttrBool(self, attrName):
        try:
            return Attribute.objects.get(aname=attrName).isBoolean
        except:
            return False

    # Returns whether this tag is deprecated
    def isDeprecated(self, tagName):
        try:
            return Element.objects.get(ename=tagName).isDeprecated
        except:
            return False

    # Returns whether this attribute is deprecated
    def isDeprecatedAttribute(self, attrName):
        try:
            return Attribute.objects.get(aname=attrName).isDeprecated
        except:
            return False

    # Returns a list of required attributes for this tag
    def requiresAttr(self, tagName):
        try:
            attrList = list()
            for attr in Attribute.objects.filter(element = Element.objects.get(ename=tagName).id).filter(isRequired=True):
                attrList.append(attr.aname)
            return attrList
        except:
            return list()

    # Returns whether this tag is self-closing
    def isSelfClosing(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isSelfClosing
        except:
            return False

    def isSingular(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isSingular
        except:
            return False

    def isMeta(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isMeta
        except:
            return False    

    def isTableElement(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isTableElem
        except:
            return False

    def isTableContainer(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isTableContainer
        except:
             return False

    def isTableSingular(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isTableSingular
        except:
            return False

    def isFormElement(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isFormElem
        except:
            return False

    def isHeadElement(self, tagName):
        try:
            return Element.objects.get(ename = tagName).isHeadElem
        except:
            return False
            
