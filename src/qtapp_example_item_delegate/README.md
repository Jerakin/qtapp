# QtApp Example Item Delegate

In this example we expand on the previous qtapp_example_model_update.

We add an ItemDelegate which we use to customize how we draw
our items.

We extend the viewmodel to send data depending on which Role is passed.

We also extend the model to download the images dynamically. We save these
in a temporary location which we clean up when we exit the app. 

![](/.github/images/qtapp_example_item_delegate.png)
