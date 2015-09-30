import maya.cmds as cmds
import maya.mel
import maya.cmds as cmds
import checkout.app as co

reload(co)

# Create custome main menu
def create_menu():

    gMainWindow = maya.mel.eval('$temp1=$gMainWindow')
    oMenu= cmds.menu(parent=gMainWindow, tearOff = True, label = 'JRG Tools')

    # Populate menu with elements

    cmds.menuItem(parent=oMenu, label='HUD', command='maya.mel.eval("animHUD")')
    cmds.menuItem(parent=oMenu, label='Checkout Scene', command='co.Checkout().run()')

cmds.evalDeferred("create_menu()")