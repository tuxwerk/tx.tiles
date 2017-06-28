.. image:: https://travis-ci.org/collective/collective.easytiler.png?branch=master
    :target: https://travis-ci.org/collective/collective.easytiler


Introduction
============
This product allows you to easily add an easyTiler content rotator to any page on a plone site using a WYSIWYG editor to design each tile.

How-to
------
On a page, click actions -> Add Tiler.  It should bring you to a tiler settings page where you can modify different aspects of the tiler and add/remove tiles using a WYSWGY editor.  Keep in mind that the tiles are fixed width so you need to specify the size you want.  Then you'll want to start adding your tiles.  To do this just click ``add new tile`` near the bottom of the page.  Once you've finished adding tiles and re-ordering tiles, click ``save`` and you should see the tiler on your page now.

You can also select a tiler view for Folder and Collection content types.  Then the tiler settings for that page will include settings to limit the amount of tiles to have and to limit the type of tiles used.

Examples
--------
Examples of this being used in the wild.

* http://www.fbi.gov/
* http://www.chicagohistory.org
* http://www.reamp.org
* http://www.rehabpro.org
* http://swca.org/

Installation
------------
* add collective.easytiler to your eggs and zcml sections
* re-run buildout
* install the product like you would any other Plone product

Uninstall
---------
* Uninstall like normal
* go to portal_setup in the zmi, click the 'import' tab, select "collective.easytiler uninstall" and click the "Import all steps" button at the bottom to perform clean up.


Easy Template Integration
-------------------------

If you'd like to add dynamic content to your tiles, add collective.easytemplate
to your eggs section in buildout, re-run buildout and restart your installation.
Then in the tiler settings make sure you enable Easy Template.

You can also render tilers in a Easy Template. The syntax is:

    {{ tiler("../front-page") }}

And for the tilerview

    {{ tilerview("../a-collection") }}


Rendering Tiler in Templates
-----------------------------

You can also easily render your tiler in a page template
if you'd like even more control over how it is displayed:

    <tal:tiler tal:content="structure context/../front-page/@@tiler_util/render_inline" />
    
And for the tilerview

    <tal:tiler tal:content="structure context/../front-page/@@tiler_util/render_tilerview_inline" />


Credits and Contributions
-------------------------
* a lot of the credit for the inspiration, styling and insight into this product belongs to Espen Moe-Nilssen 
