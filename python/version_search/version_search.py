
import os
import json
import sgtk

from sgtk.platform.qt import QtCore, QtGui

from .ui.version_search_widget import Ui_VersionSearchWidget
from .version_search_proxy import VersionTreeProxyModel

from ..views.grouped_list_view.grouped_list_view import GroupedListView
from ..views.grouped_list_view.group_widget import GroupWidget

from ..search_widget.search_widget import SearchWidget

shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "shotgun_model",
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

        self._init_ui()
        self._connect_signals()

        model_filters = [['project', 'is', SHOW],
                         ['entity', 'is', SHOT]]

        self._version_model._load_data('Version',
                                       model_filters,
                                       ['sg_step', 'code'],
                                       ['type'])

        self._version_model._refresh_data()

    def _init_ui(self):

        self._main_layout = QtGui.QVBoxLayout(self)
        self._search_layout = QtGui.QHBoxLayout(self)
        self._version_layout = QtGui.QHBoxLayout(self)

        self._search_widget = SearchWidget(self)
        self._search_layout.addWidget(self._search_widget)

        self._version_view = QtGui.QTreeView(self)
        self._version_proxy = VersionTreeProxyModel(self._version_view)
        self._version_model = shotgun_model.ShotgunModel(self._version_view,
                                                         download_thumbs=False,
                                                         bg_load_thumbs=False)

        self._version_proxy.setFilterWildcard('*')
        self._version_proxy.setSourceModel(self._version_model)
        self._version_view.setModel(self._version_proxy)
        self._version_layout.addWidget(self._version_view)

        self._main_layout.addLayout(self._search_layout)
        self._main_layout.addLayout(self._version_layout)

        self.setLayout(self._main_layout)

        # TODO: Make a not shitty style sheet
        #self.setObjectName('version_search_widget')
        #self.view.setObjectName('version_view')
        #self._load_stylesheet()

    def _connect_signals(self):
        self._search_widget.search_edited.connect(self._search_edited)

    def _search_edited(self, *args, **kwargs):
        print 'search edited signal!'
        print 'args:', args
        print 'kwargs:', kwargs

    def _load_stylesheet(self):
        """
        Loads in the widget's master stylesheet from disk.
        """
        qss_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "style.qss"
        )
        try:
            f = open(qss_file, "rt")
            qss_data = sgtk.platform.current_bundle().engine._resolve_sg_stylesheet_tokens(
                f.read(),
            )
            print qss_data
            self.setStyleSheet(qss_data)
        finally:
            f.close()

