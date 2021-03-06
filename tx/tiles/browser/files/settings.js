function tx_tile_remove() {
  if (!window.confirm($(this).attr('data-confirm-text')))
    return false;

  $.get($(this).attr('href') + '?ajax=true', {}, function(data, status) { });
  $(this).closest("li").remove();
  return false;
}

function tx_tile_sortable() {
  $("#tx-tiles-widget ul").sortable({
    connectWith: "#tx-tiles-widget ul",
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
        url: $('#tx-tiles-widget').attr('data-order-tiles-url'),
        type: 'POST',
        data: {
          order: order
        }
      }); 
    }
  });
}

$(document).ready(function(){
  $("#tx-tiles-widget a.tx-tile-remove").click(tx_tile_remove);
  tx_tile_sortable();
  // $('.tile-buttons a.tile-edit, .tile-add-buttons a.tile-add').prepOverlay({
  //   subtype: 'ajax',
  //   filter: '#content>*',
  //   formselector: 'form',
  //   config:{expose:{color:'#00f'}}
  // });
});
