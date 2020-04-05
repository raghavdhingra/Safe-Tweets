// alert()
const addSuspect = (username,id) => {
    document.getElementById("loader-container").classList.add("display-flex");
    $.get(`/api/twitter/add-suspect/${username}`, function( data ) {
        if (data.code == 0){
            document.getElementById("loader-container").classList.remove("display-flex");
            // swal("Added!", `Username: ${username} has been added to the suspect list.`, "success");
            swal({
                title: "Added!",
                text: `Username: ${username} has been added to the suspect list.`,
                icon: "success",
            }).then(()=>{
                document.getElementById(`suspect-${username}`).value = "Remove from Suspect List";
            });
        }
        else if (data.code == 1){
            swal({
                    title: "User Exists",
                    text: `Username: ${username} already exists. Do you want to remove the user from the suspect list?`,
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        $.get(`/api/twitter/delete-suspect/${username}`,function(){
                            swal( `Username: ${username} has been deleted.`, {
                            icon: "success",
                            })
                            .then(()=>{
                                document.getElementById("loader-container").classList.remove("display-flex");
                                document.getElementById(`suspect-${username}`).value = "Add to Suspect List";
                            });
                        })
                    } else {
                        swal(`Username: ${username} has been retained in the suspect list.`);
                        document.getElementById("loader-container").classList.remove("display-flex");
                        document.getElementById(`suspect-${username}`).value = "Remove from Suspect List";
                    }
                });
            }
        else{
            swal({
                title: "Unknown Error",
                text: "Something Wrong happened.",
                icon: "warning",
            });
        }
    });
}

const addSuspect1 = (username,id) => {
    document.getElementById("loader-container").classList.add("display-flex");
    $.get(`/api/twitter/add-suspect/${username}`, function( data ) {
        if (data.code == 0){
            document.getElementById("loader-container").classList.remove("display-flex");
            // swal("Added!", `Username: ${username} has been added to the suspect list.`, "success");
            swal({
                title: "Added!",
                text: `Username: ${username} has been added to the suspect list.`,
                icon: "success",
            }).then(()=>{
                document.getElementById(`suspect-${username}`).innerText = "Remove from Suspect List";
            });
        }
        else if (data.code == 1){
            swal({
                    title: "User Exists",
                    text: `Username: ${username} already exists. Do you want to remove the user from the suspect list?`,
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        $.get(`/api/twitter/delete-suspect/${username}`,function(){
                            swal( `Username: ${username} has been deleted.`, {
                            icon: "success",
                            })
                            .then(()=>{
                                document.getElementById("loader-container").classList.remove("display-flex");
                                document.getElementById(`suspect-${username}`).innerText = "Add to Suspect List";
                            });
                        })
                    } else {
                        swal(`Username: ${username} has been retained in the suspect list.`);
                        document.getElementById("loader-container").classList.remove("display-flex");
                        document.getElementById(`suspect-${username}`).innerText = "Remove from Suspect List";
                    }
                });
            }
        else{
            swal({
                title: "Unknown Error",
                text: "Something Wrong happened.",
                icon: "warning",
            });
        }
    });
}

const waitKey = ()=>{
    document.getElementById("loader-container").classList.add("display-flex");
};