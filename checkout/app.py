import maya.cmds as cmds
import pymel.core as pm
import os
import shutil
import sgtk

class Checkout(object):
    
    def __init__ (self):

        # tk  = sgtk.sgtk_from_path(pm.sceneName())

        self.root_project_path = os.path.normpath('//180net1/Collab')
        self.project_name = 'sX_JRG'
        # self.project_path = tk.roots['primary']

        self.project_path = '//180net1/Collab/sX_JRG'


        # Ask user where he want to copy the project
        # Return absolute directory path
        self.destination = pm.fileDialog2(dialogStyle=2, fileMode=3, okCaption='OK')[0]
        
        # List of dictionaries for all references in the scene
        self.refs = []

        self.project_env_var = 'PROJECT'

        os.environ[self.project_env_var] = self.project_path


    def _change_root(self, path, old_root, new_root):

        old_root = os.path.normpath(old_root)
        new_root = os.path.normpath(new_root)

        new_path = path.replace(old_root, new_root)

        return new_path


    def make_folders(self, path):

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))


    def scan_scene(self):
    
        # first let's look at maya references
        for x in pm.listReferences():
            node_name = x.refNode.longName()
        
            # get the path and make it platform dependent
            # (maya uses C:/style/paths)
            maya_path = x.path.replace("/", os.path.sep)
            self.refs.append( {"node": node_name, "type": "reference", "path": maya_path})
        
        # now look at file texture nodes
        for file_node in cmds.ls(l=True, type="file"):
            # ensure this is actually part of this scene and not referenced
            if cmds.referenceQuery(file_node, isNodeReferenced=True):
                # this is embedded in another reference, so don't include it in the breakdown
                continue
        
            # get path and make it platform dependent (maya uses C:/style/paths)
            path = cmds.getAttr("%s.fileTextureName" % file_node).replace("/", os.path.sep)
        
            self.refs.append( {"node": file_node, "type": "file", "path": path})

        # Append scene file
        self.refs.append( {"node": None, "type": "scene", "path": pm.sceneName()})
        
        return self.refs

  
    def copy(self):

        for ref in self.refs:

            old_path = os.path.normpath(ref['path'])

            new_path = self._change_root(old_path, 
                                   self.root_project_path, 
                                   self.destination)

            
            self.make_folders(new_path)

            shutil.copy(old_path, new_path)

            print '%s\ncopied to\n%s' % (old_path, new_path)

        print 'Copy is done!'

    
    # Make all reference paths relative to PROJECT environmental variable
    def remap_paths(self):

        for ref in self.refs:

            if ref['type'] == 'reference':
                r = pm.FileReference(ref['node'])

                r.unload()
                r.replaceWith(os.path.normpath(ref['path']).replace(os.path.normpath(self.project_path), '$' + self.project_env_var), loadReferenceDepth='none')
                r.load()

    def copy_run_maya_client(self):


        project_script_path
        script_name
        run_maya_client_path = os.path.join(self.project_path, 'script', 'run_maya_client.bat')

        shutil.copy(self.run_maya_client_path, new_path)


    def make_launcher(self):

        content = '''@echo off
set PROJECT=%cd%
set MAYA_PROJECT=%cd%
"C:\\Program Files\\Autodesk\\Maya2015\\bin\\maya.exe"'''

        script_name = 'RunMayaClient.bat'
        script = os.path.join(self.destination, self.project_name, script_name)

        with open(script, 'w') as f:
            f.write(content)


    def run(self):

        self.scan_scene()
        self.remap_paths()
        pm.saveFile()
        self.copy()
        self.make_launcher()