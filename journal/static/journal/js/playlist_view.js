let timer = $('.timer');
let pause_timer = $('#pause_timer');
let start_timer = $('#start_timer');

timer.countimer({autoStart : false});
pause_timer.hide();
$('#rate_form').hide();
$('#back_session').hide();
$('#done').hide();


start_timer.on('click', function() {
  if (timer.countimer('stopped')) {
      timer.countimer('resume')
  } else {
       timer.countimer('start')
  }
  start_timer.hide();
  pause_timer.show();
    });

pause_timer.on('click', function() {
  timer.countimer('stop');
  start_timer.show();
  pause_timer.hide();
});

function rate_session_acc() {
    timer.countimer('stop');
    start_timer.hide();
    pause_timer.hide();
    $('#session_form').hide();
    $('#rate_form').show();
    $('#rate_session').hide();
    $('#back_session').show();
    $('#done').show();

}

function back_session_form() {
    start_timer.show();
    pause_timer.hide();
    $('#session_form').show();
    $('#rate_form').hide();
    $('#rate_session').show();
    $('#back_session').hide();
    $('#done').hide();

}

$('#modalSession').on('show.bs.modal', function(e) {
    let item_id = $(e.relatedTarget).data('item-id');
    if (item_id) {
        $(e.currentTarget).find('input[name="id"]').val(item_id);
    }
});


	jQuery(document).ready(function($){

	$(".btnrating").on('click',(function(e) {

	var previous_value = $("#selected_rating").val();

	var selected_value = $(this).attr("data-attr");
	$("#selected_rating").val(selected_value);

	$(".selected-rating").empty();
	$(".selected-rating").html(selected_value);

	for (i = 1; i <= selected_value; ++i) {
	$("#rating-star-"+i).toggleClass('btn-success');
	$("#rating-star-"+i).toggleClass('btn-');
	}

	for (ix = 1; ix <= previous_value; ++ix) {
	$("#rating-star-"+ix).toggleClass('btn-success');
	$("#rating-star-"+ix).toggleClass('btn-default');
	}

	}));


});