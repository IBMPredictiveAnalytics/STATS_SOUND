#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2020
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/


"""STATS SOUND extension command"""

__author__ =  'JKP'
__version__=  '1.0.1'

# history
# 07-apr-2012 original version


helptext = """
This command plays the selected sound when executed.  It is only
available on Windows.

STATS SOUND 
[TYPE={DEFAULT*|EXCLAMATION|ASTERISK|HAND|QUESTION}]
or
FILE="filespec"
[/HELP]


Example:
STATS SOUND TYPE=EXCLAMATION. 

Specify either TYPE or FILE.  If nothing is specified, the Windows Beep sound is produced.
FILE must specify a wav file.

Using TYPE, the sound played is whatever is associated with the selected sound according
to the settings in the Windows Control Panel Sounds dialog.

If both TYPE and FILE are specified, FILE is played first.

HELP displays this help and does nothing else
"""

from extension import Template, Syntax, processcmd
from spssaux import FileHandles


def sound(soundtype=None, filespec=None):
    """Play selected sound"""
    
        # debugging
    # makes debug apply only to the current thread
    #try:
        #import wingdbstub
        #if wingdbstub.debugger != None:
            #import time
            #wingdbstub.debugger.StopDebug()
            #time.sleep(2)
            #wingdbstub.debugger.StartDebug()
        #import thread
        #wingdbstub.debugger.SetDebugThreads({thread.get_ident(): 1}, default_policy=0)
        ## for V19 use
        #SpssClient._heartBeat(False)
    #except:
        #pass
    
    # imported within function so that localization and error handling are enabled
    try:
        import winsound
    except:
        raise SystemError(_("""This command is only available on Windows"""))
    
    sounds = {None:winsound.MB_OK, "default":winsound.MB_OK, "exclamation":winsound.MB_ICONEXCLAMATION,
        "asterisk": winsound.MB_ICONASTERISK, "hand":winsound.MB_ICONHAND,
        "question":winsound.MB_ICONQUESTION}
    
    if filespec:
        fh = FileHandles()
        filespec = fh.resolve(filespec)
        winsound.PlaySound(filespec, winsound.SND_FILENAME)
        if soundtype is None:
            return

    winsound.MessageBeep(sounds[soundtype])

def Run(args):
    """Execute the STATS SOUND extension command"""

    args = args[list(args.keys())[0]]

    oobj = Syntax([
        Template("TYPE", subc="",  ktype="str", var="soundtype", 
            vallist=["default","asterisk", "exclamation","hand","question"]),
        Template("FILE", subc="", ktype="literal", var="filespec"),
        Template("HELP", subc="", ktype="bool")])
    
    #enable localization
    global _
    try:
        _("---")
    except:
        def _(msg):
            return msg
    # A HELP subcommand overrides all else
    if "HELP" in args:
        #print helptext
        helper()
    else:
        processcmd(oobj, args, sound)

def helper():
    """open html help in default browser window
    
    The location is computed from the current module name"""
    
    import webbrowser, os.path
    
    path = os.path.splitext(__file__)[0]
    helpspec = "file://" + path + os.path.sep + \
         "markdown.html"
    
    # webbrowser.open seems not to work well
    browser = webbrowser.get()
    if not browser.open_new(helpspec):
        print(("Help file not found:" + helpspec))
try:    #override
    from extension import helper
except:
    pass        