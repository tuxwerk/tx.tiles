TX Tiles configuration and layout
=================================

Homepage: https://github.com/tuxwerk/tx.tiles

Configuration
-------------

You can set global CSS classes for the tiles (column layouts) and predefined CSS classes for individual tiles (See section: Layout). Also the scale factor for image uploads can be configured.

Security
--------

The Add-On defines following permissions:

*tx.tiles: Add tiles*

Adding and removing tiles on content. (Default: Site Administrator and Editor)

*tx.tiles: Edit tiles*

Editing of tiles. (Default: Site Administrator and Editor)

*tx.tiles: Manage tiles settings*

Can manage the configuration in Plone Control Panel. (Default: Site Administrator)

Layout
------

For all tiles
~~~~~~~~~~~~~

Tiles on a page can be configured by assigning a CSS class. The classes and display names are configured through the Plone Control Panel. The add on has the following predefined configurations:

* tx-tiles-2-columns
* tx-tiles-3-columns
* tx-tiles-4-columns

For individual tiles
~~~~~~~~~~~~~~~~~~~~

CSS classes can also be assigned to individual tiles. The classes and display names are configured through the Plone Control Panel. The add on has a predefined example class:

* tx-tile-important

CSS Styles
~~~~~~~~~~

The tiles layout can be altered by CSS. You can define new CSS classes in your theme product and set them in the Plone Control Panel.

You can use following CSS to overload the height of tiles (Add the CSS class 'tx-custom-height' in the add on configuration)::

  /* set aspect ratio 4:3 */
  .tx-tiles-container.tx-custom-height {
    padding-top: 75%;
  }

Individual tiles can be styled as following (Add the CSS class 'red-tile' in the individual tile configuration)::

  /* show heading on red background */
  .red-tile h2.tx-tile-heading {
    background: red;
  }
  
The tiles are rendered with following HTML Code::

 <ul class="tx-tiles-container tx-tiles-UID GLOBAL-TILES-CLASS">
   <li>
     <div class="tx-tile INDIVIDUAL-TILE-CLASS">
       <div class="tx-tile-content">
         <h2 class="tx-tile-heading">Heading</h2>
         <div class="tx-tile-text">
           <p>
	     A paragraph.
	   </p>
         </div>
         <img class="tx-tile-image" src="...">
       </div>
     </div>
   </li>
   ...
 </ul>
