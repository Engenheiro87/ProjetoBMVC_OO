console.log("(!) JavaScript loaded.");
document.addEventListener("DOMContentLoaded", function(){
// waits for the page to load.
    console.log("(!) DOMContent has been loaded.");

    let selected_exercises = {}; // empty selected_exercises dict/idk

    const wc_buttons =  
        document.querySelectorAll("wc-exercise-div-btn"); // gets all buttons inside all template divs

    wc_buttons.forEach(button=>{
        console.log(`Applying \"for each\" on button ${button}`);
        button.addEventListener("click", function(){
            const type =
                button.dataset.type; // checks if it's either a "select", a "plus" or "minus" button.

            const exerciseId =
                button.dataset.exerciseId; // gets the exercise_id of the button (to relate components better)

            const reps_label = 
                document.getElementById(`REPS_${button.dataset.exerciseId}`); // gets the reps label for that template for updating.

            function update_rlabel(){ // updates the reps label.
                reps_label.textContent =
                    selected_exercises[exerciseId].reps;
            };
            
            if (type === "select") {
                console.log(`selecting exercise ${exerciseId}!`);
                
                if (selected_exercises[exerciseId]){
                    delete selected_exercises[exerciseId];
                }
                else {
                    selected_exercises[exerciseId] = {
                        "reps":12,
                    };
                }
            }
            else if (type === "plus") {
                console.log(`Attempting to increase exercise ${exerciseId}`);

                const exercise = 
                    selected_exercises[exerciseId];
                
                if (!exercise) {
                    console.log(`Attempt to press plus on a non-existent exercise ${exerciseId}`);
                    return;
                }

                exercise.reps++;
            }
            else if (type === "minus") {
                console.log(`Attempt to decrease exercise ${exerciseId}`);

                const exercise =
                    selected_exercises[exerciseId];
                
                if (!exercise){
                    return;
                };

                exercise.reps--;
            }

            update_rlabel();
        });
    });
    

    // submit part
//     const submit_btn =
//         document.querySelector(".submit-exercise");

//     submit_btn.addEventListener("click", function(){
//         console.log("Clicked to submit");
        
//         fetch("/create_workout", {
//             method: "POST",

//             headers:{
//                 "Content-Type":"application/json"
//             },

//             body: JSON.stringify({ // apparently converts "objects" into strings? Apparently HTTP can only send texts
//                 exercises:selected_exercises
//             })
//             // Python is going to receive a dictionary with an "exercises" list, the rest is history.
//         });
    
// });

});
