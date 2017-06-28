function tx_tile_remove() {
  if (!window.confirm("Are you sure you want to remove this tile?"))
    return false;

  $.get($(this).attr('href') + '?ajax=true', {}, function(data, status) {
  });
  $(this).closest("li").remove();
  return false;
}

function tx_tile_sortable() {
  $("#tx-tiles-widget ul").sortable({
    items: 'li',
    placeholder: 'sortable-placeholder',
    forcePlaceholderSize: true,
    update: function(event, ui) {
      var order = [];
      var tiles = $('#tx-tiles-widget li');
      for(var i=0; i<tiles.length; i++){
        order.push(tiles.eq(i).attr('data-index'));
      }
      $.ajax({
        url: $('base').attr('href') + '/../@@tx-tiles/all/@@order-tiles',
        type: 'POST',
        data: {
          order: order
        },
        // success: function(data){
        //     $.ajax({
        //         url: window.location.toString(),
        //         success: function(data){
        //             var dom = $(data);
        //             $('#tilelist').replaceWith(dom.find('#tilelist'));
        //             enableTiles();
        //         }
        //     });
        // }
      }); 
    }
  });
}

$(document).ready(function(){
  $("#tx-tiles-widget a.tile-remove").click(tx_tile_remove);
  tx_tile_sortable();
  // $('.tile-buttons a.tile-edit, .tile-add-buttons a.tile-add').prepOverlay({
  //   subtype: 'ajax',
  //   filter: '#content>*',
  //   formselector: 'form',
  //   config:{expose:{color:'#00f'}}
  // });
});
