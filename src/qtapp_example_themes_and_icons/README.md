# QtApp Example Themes and Icons

In this example we add a simple theme and some icons.

The qss illustrates how to use images from add search paths as well how to use properties.
We can [use properties](/src/qtapp_example_themes_and_icons/view/__init__.py) to enable any kind of QSS, in this example we only change the colors.

We set the image on the QAction through the search path.

We also apply both our company qss, and the apps. This is simply done by loading both files and joining the strings.

By doing this we can also "overwrite" our company's Qss definitions with a more custom style.
In the future if the company updates the theme you would only need to replace the old one.  

![](/.github/images/qtapp_example_themes_and_icons.png)
