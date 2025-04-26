# QtApp Example Dynamic Table Size

In this example we expand on the previous qtapp_example_item_delegate example.

We subclass `QtWidgets.QTableView` to override the `resizeEvent` which we use to
set our new `size` attribute on our sourceModel. The model will use this size when
calculating how many columns to display.

> [!NOTE]
> This kind of approach only works if all our items are of the same width.
> 

> [!NOTE]
> We are also set `self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)`
> which stretches the items, this can look good or bad depending on your items. 
> 

![](/.github/images/qtapp_example_dynamic_table_size.png)
