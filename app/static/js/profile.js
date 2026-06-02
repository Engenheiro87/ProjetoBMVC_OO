document.addEventListener("DOMContentLoaded", function(){

    const trash_btns = 
        document.querySelectorAll(".delete-btn");
    
    trash_btns.forEach(button=>{
        let deleted =
            false;
        button.addEventListener("click", function(){
            if (deleted){
                return;
            };

            const workout_id = 
                button.dataset.workoutId;
            
            fetch("/delete_workout", {
                method: "POST",

                headers: {
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    workout_id: workout_id,
                })
            })
            .then(response=>response.json())
            .then(data=>{
                if (data["sucess"]){
                    window.location.href =
                        "/profile"
                }   
                else{
                    console.log(
                        `Error message: ${data["error"]}`
                    )
                }
                window.location.href = "/profile"
            });
                
        });
    });
});