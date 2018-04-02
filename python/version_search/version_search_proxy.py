
import sgtk

from sgtk.platform.qt import QtCore, QtGui

from ..models.hierarchical_filtering_proxy_model import HierarchicalFilteringProxyModel

class VersionTreeProxyModel(HierarchicalFilteringProxyModel):

    def __init__(self, parent=None):
        super(VersionTreeProxyModel, self).__init__(parent=parent)

    def _is_row_accepted(self, src_row, src_parent_idx, parent_accepted):

        # top level node, go ahead and display it
        # TODO: How to hide parents that end up having no children?
        if not parent_accepted:
            return True

        model = self.sourceModel()

        version_code = model.data(model.index(src_row, 0, src_parent_idx))
        code_matches = self.filterRegExp().exactMatch(version_code)

        return code_matches
