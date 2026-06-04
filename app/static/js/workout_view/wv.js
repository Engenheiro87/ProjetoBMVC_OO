document.addEventListener("DOMContentLoaded", function(){
    const timer_btns =
        document.querySelectorAll(".timer");

    const done_btns =
        document.querySelectorAll(".done");

    let working_timers = 
        {};
    
    timer_btns.forEach(button => {
        let rest_time =
            parseInt(button.dataset.time);
            
        const exercise_id
            = button.dataset.exerciseId;
        
        let alarm_sound = 
            null;

        function display_time(){
            const mins =
                Math.floor(rest_time/60).toString().padStart(2, 0);
            
            const secs =
                Math.floor(rest_time % 60).toString().padStart(2, 0)
            
            button.textContent =
                `${mins}:${secs}`
        };

        function kill_timer(){
            const interval =
                working_timers[exercise_id];
            
            if (interval){
                clearInterval(interval);
                delete working_timers[exercise_id];
                rest_time = 
                    button.dataset.time;
                display_time();
                return;
            };
        };

        function play_alarm(){
            if (alarm_sound){
                return;
            };
            alarm_sound = 
                new Audio(
                    "/static/audio_files/alarm_audio.mp3"
                );
            
            alarm_sound.play();

            alarm_sound.onended = function(){
                alarm_sound = null;
            };
        };

        function stop_alarm(){
            if (!alarm_sound){
                return;
            };
            alarm_sound.pause();
            alarm_sound.currentTime = 0;
            alarm_sound = null;
        };

        button.addEventListener("click", function(){ 
            if (working_timers[exercise_id]){
                kill_timer();
            }
            else {
                stop_alarm();
                working_timers[exercise_id] =
                    setInterval(function(){
                        if (rest_time <= 0){
                            kill_timer();
                            play_alarm();
                            return;
                        };
                        rest_time--;
                        display_time();
                    }, 1000);
            };
        });
    });
});