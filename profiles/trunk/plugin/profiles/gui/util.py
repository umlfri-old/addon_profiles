def FixTreeViewSelectionOnRightClick(treeView, x, y):
    path = treeView.get_path_at_pos(x, y)
    selection = treeView.get_selection()
    if path:
        if not selection.path_is_selected(path[0]):
            selection.unselect_all()
            selection.select_path(path[0])
    else:
        selection.unselect_all()
