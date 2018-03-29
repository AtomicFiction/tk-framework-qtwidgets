
import os
import json
import sgtk

from sgtk.platform.qt import QtCore, QtGui

from .ui.version_search_widget import Ui_VersionSearchWidget

from ..views.grouped_list_view.group_widget import GroupWidget
from ..views.grouped_list_view.grouped_list_view import GroupedListView

shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "shotgun_model",
)

shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "shotgun_globals",
)

task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "task_manager",
)

shotgun_data = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "shotgun_data",
)

settings = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "settings",
)

models = sgtk.platform.current_bundle().import_module("models")

# temp imports/globals for testing
import shotgun_api3.shotgun
url = 'https://atomic-staging.shotgunstudio.com'
sg_conn = shotgun_api3.shotgun.Shotgun(url,
                                       login='admin',
                                       password='@F$Taging')

SHOW = sg_conn.find_one('Project', [['name', 'is', 'default']])
SHOT = sg_conn.find_one('Shot', [['code', 'is', 'G_01'],
                                 ['project', 'is', SHOW]])

print SHOW
print SHOT

class VersionSearchWidget(QtGui.QWidget):

    def __init__(self, parent=None, engine=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_VersionSearchWidget()
        self.ui.setupUi(self)

        self.view = QtGui.QTreeView(self)
        self.version_model = shotgun_model.ShotgunModel(self.view,
                                                        download_thumbs=False,
                                                        bg_load_thumbs=False)

        self.view.setModel(self.version_model)

        self._main_layout = QtGui.QVBoxLayout(parent)
        self._main_layout.addWidget(self.view)
        self.setLayout(self._main_layout)

        self.version_model.data_refreshed.connect(self._foo)

        model_filters = [['project', 'is', SHOW],
                         ['entity', 'is', SHOT]]

        self.version_model._load_data('Version',
                                      model_filters,
                                      [['sg_step'], ['code']],
                                      ['type'])

        self.version_model._refresh_data()


    def _foo(self):
        print 'foo'
'''
        self.ui = Ui_VersionSearchWidget()
        self.ui.setupUi(self)

        self.group_widget = GroupWidget()


        self.version_model = shotgun_model.ShotgunModel(self,
                                                        download_thumbs=False,
                                                        bg_load_thumbs=False)

        model_filters = [['project', 'is', SHOW],
                         ['entity', 'is', SHOT]]


        self.version_model._load_data('Version',
                                      model_filters,
                                      ['sg_step', 'code'],
                                      ['code'])

        self.view = QtGui.QTreeView(self)

        self.proxy_model = models.HierarchicalFilteringProxyModel(parent=self.view)
        self.proxy_model.setSourceModel(self.version_model)

        self.view = GroupedListView(self)
        #self.view.setModel(self.proxy_model)

        self._main_layout = QtGui.QVBoxLayout(parent)
        self._main_layout.addWidget(self.view)
        self.setLayout(self._main_layout)
'''



