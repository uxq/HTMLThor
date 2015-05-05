from django.db import models

class Element(models.Model):
    ename = models.CharField(max_length=50)
    isDeprecated = models.BooleanField()
    isSelfClosing = models.BooleanField()
    isSingular = models.BooleanField()
    isMeta = models.BooleanField()
    isHeadElement = models.BooleanField()
    isFormElement = models.BooleanField()
    isTableElement = models.BooleanField()
    isTableContainer = models.BooleanField()
    isTableSingular = models.BooleanField()
    
class Attribute(models.Model):
    aname = models.CharField(max_length=50)
    isDeprecated = models.BooleanField()
    isGlobal = models.BooleanField()
    isRequired = models.BooleanField()
    isBoolean = models.BooleanField()
    isScript = models.BooleanField()

    element = models.ForeignKey(Element)

class Error(models.Model):
    message = models.CharField(max_length=200)
    ERROR_OPTIONS = (
    ('BRO', 'Broken'),
    ('DEP', 'Deprecated'),
    ('SEM', 'Semantic'),
    ('SYN', 'Syntax'),
    ('WAR', 'Warning'))
    errorType = models.CharField(max_length=3,
                                      choices=ERROR_OPTIONS)
    


    

    
