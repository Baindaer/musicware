let timer = $('.timer');
let pause_timer = $('#pause_timer');
let start_timer = $('#start_timer');
timer.countimer({autoStart : false});
pause_timer.hide();

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