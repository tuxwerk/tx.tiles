function tx_slide_remove() {
  if (!window.confirm("Are you sure you want to remove this slide?"))
    return false;

  $.get($(this).attr('href') + '?ajax=true', {}, function(data, status) {
  });
  $(this).closest("li").remove();
  return false;
}

function tx_slide_sortable() {
  $("#tx-slider-widget ul").sortable({
    items: 'li',
    placeholder: 'sortable-placeholder',
    forcePlaceholderSize: true,
    update: function(event, ui) {
      var order = [];
      var slides = $('#tx-slider-widget li');
      for(var i=0; i<slides.length; i++){
        order.push(slides.eq(i).attr('data-index'));
      }
      $.ajax({
        url: $('base').attr('href') + '/../@@tx-slides/all/@@order-slides',
        type: 'POST',
        data: {
          order: order
        },
        // success: function(data){
        //     $.ajax({
        //         url: window.location.toString(),
        //         success: function(data){
        //             var dom = $(data);
        //             $('#slidelist').replaceWith(dom.find('#slidelist'));
        //             enableSlides();
        //         }
        //     });
        // }
      }); 
    }
  });
}

$(document).ready(function(){
  $("#tx-slider-widget a.slide-remove").click(tx_slide_remove);
  tx_slide_sortable();
  // $('.slide-buttons a.slide-edit, .slide-add-buttons a.slide-add').prepOverlay({
  //   subtype: 'ajax',
  //   filter: '#content>*',
  //   formselector: 'form',
  //   config:{expose:{color:'#00f'}}
  // });
});
