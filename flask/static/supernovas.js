// Make ajax request to api to load all supernova in database and create a boostrap table

// TODO - make ajax request to api to load all supernovas in database
$.ajax({
    url: "/api/sn",
    type: "GET",
    dataType: "json",
    sucess: data => {
        console.log(data)
        // TODO - create a boostrap table
    },
})