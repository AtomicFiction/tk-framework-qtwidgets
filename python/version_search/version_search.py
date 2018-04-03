
import os
import json
import sgtk

from sgtk.platform.qt import QtCore, QtGui

from .version_search_proxy import VersionTreeProxyModel

from ..search_widget.search_widget import SearchWidget

shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "shotgun_model",
)


models = sgtk.platform.current_bundle().import_module("models")

class VersionSearchMenu(QtGui.QMenu):

    version_selected = QtCore.Signal(list)

    FIELDS = ['sg_uploaded_movie_frame_rate',
              'sg_first_frame',
              'sg_movie_has_slate',
              'entity']

    FILTERS = ['sg_path_to_movie', 'is_not', None]

    def __init__(self, parent=None, engine=None):
        QtGui.QMenu.__init__(self, parent)

        self._init_ui()
        self._connect_signals()

        # TODO: expose convenience methods to version_model._load_data
        # and version_model._refresh_data; can call them
        # manually

    def _init_ui(self):

        self._main_layout = QtGui.QVBoxLayout(self)
        self._search_layout = QtGui.QHBoxLayout(self)
        self._version_layout = QtGui.QHBoxLayout(self)

        self._search_widget = SearchWidget(self)
        self._search_layout.addWidget(self._search_widget)

        self._version_view = QtGui.QTreeView(self)
        self._version_proxy = VersionTreeProxyModel(self._version_view)
        self.version_model = shotgun_model.ShotgunModel(self._version_view,
                                                        download_thumbs=False,
                                                        bg_load_thumbs=False)

        self._version_proxy.setFilterWildcard('*')
        self._version_proxy.setSourceModel(self.version_model)
        self._version_view.setModel(self._version_proxy)
        self._version_layout.addWidget(self._version_view)

        self._main_layout.addLayout(self._search_layout)
        self._main_layout.addLayout(self._version_layout)

        self.setLayout(self._main_layout)

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        # TODO: How to automatically make all the contents visible when
        # the model reloads data?

        # TODO: Set menu size based on model contents

    def _connect_signals(self):
        self._search_widget.search_edited.connect(self._set_proxy_regex)
        self._search_widget.search_changed.connect(self._set_proxy_regex)

        self._version_view.doubleClicked.connect(self._version_selected)

    def _set_proxy_regex(self, search_args):
        self._version_proxy.invalidateFilter()
        regex = '*{args}*'.format(args=search_args)
        self._version_proxy.setFilterWildcard(regex)
        self._version_proxy.invalidateFilter()

    def _version_selected(self, event):
        item = self.version_model.itemFromIndex(self._version_proxy.mapToSource(event))
        sg_data = item.get_sg_data()
        print sg_data

        self.version_selected.emit([sg_data])



