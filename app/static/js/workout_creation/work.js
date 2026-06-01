const MAX_EXERCISES =
    12;

document.addEventListener("DOMContentLoaded", function(){
// waits for the page to load.

    let selected_exercises = {}; // empty selected_exercises dict/idk
    let created = false;

    const wc_buttons =  
        document.querySelectorAll(".wc-exercise-div-btn"); // gets all buttons inside all template divs

    const wc_submit = 
        document.querySelector(".wc-exercise-submit"); // the submit button

    wc_buttons.forEach(button=>{
        const type =
            button.dataset.type; // checks if it's either a "select", a "plus" or "minus" button.

        const exerciseId =
            button.dataset.exerciseId; // gets the exercise_id of the button (to relate components better)

        const reps_label = 
            document.getElementById(`REPS_${button.dataset.exerciseId}`); // gets the reps label for that template for updating.

        function update_rlabel(){ // updates the reps label.
            const exercise_entity =
                selected_exercises[exerciseId];

            if (!exercise_entity){
                reps_label.textContent = 
                    "-"
                return;
            }
            reps_label.textContent =
                `${exercise_entity.reps} rep${exercise_entity.reps>1 ? "s":""}`;
        };

        function update_submit(){
            exercises_length = Object.keys(selected_exercises).length;
            wc_submit.textContent =
                `CREATE (${exercises_length})` // updates the submit button
            if (exercises_length>0 && exercises_length<=MAX_EXERCISES){
                wc_submit.classList.add("ready");
            }
            else{
                wc_submit.classList.remove("ready");
            };
        };
        
        button.addEventListener("click", function(){
            if (type === "select") {

                button.classList.toggle("selected");
                

                if (selected_exercises[exerciseId]){
                    delete selected_exercises[exerciseId];
                    update_rlabel();
                    update_submit();
                    return;
                }
                else {
                    selected_exercises[exerciseId] = {
                        "reps": parseInt(button.dataset.reps),
                        "exercise_type": button.dataset.exerciseType,
                    };
                    update_submit();
                }
            }
            else if (type === "plus") {
                const exercise = 
                    selected_exercises[exerciseId];
                
                if (!exercise) {
                    return;
                }

                exercise.reps++;
            }
            else if (type === "minus") {
                const exercise =
                    selected_exercises[exerciseId];
                
                if (!exercise){
                    return;
                }

                if (exercise.reps>1){
                    exercise.reps--;
                }
            }

            update_rlabel();
        });
    });
    

    // submit part

    wc_submit.addEventListener("click", function(){
        exercises_length = 
            Object.keys(selected_exercises).length;

        if (exercises_length < 1 || exercises_length > MAX_EXERCISES){
            return;
        }
        else if (created)
        {
            return;
        }

        wc_submit.textContent = 
            "CREATING...";
        wc_submit.classList.remove("ready");
        
        created = 
            true;
            
        fetch("/create_workout", {
            method: "POST",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify({ // apparently converts "objects" into strings? Apparently HTTP can only send texts
                exercises:selected_exercises
            })
            // Python is going to receive a dictionary with an "exercises" list, the rest is history.
        })
        .then(response=>response.json())
        .then(data=>{

            if (data["sucess"]){
                window.location.href = 
                    "/profile";
            }
            else {
                console.log(
                    `Error message: ${data["error"]}`
                );
                
                window.location.href = 
                    "/workout_creation";
            };
        });
    
    });

});
