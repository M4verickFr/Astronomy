// Make ajax request to api to load all supernova in database and create a boostrap table

// TODO - make ajax request to api to load all supernovas in database
$.ajax({
    url: "/api/sn?active=true",
    type: "GET",
    dataType: "json",
    success: data => {
        //console.log(data)
        for (let d of data){
            let tr = document.createElement("tr")
            tr.onclick = function(){
                location.href="./viewer?ra=" + d.ra_degree + "&decl=" + d.decl_degree
            }
            let name = document.createElement("td")
            name.innerHTML = d.name
            let galaxy = document.createElement("td")
            galaxy.innerHTML = d.galaxy
            let date = document.createElement("td")
            date.innerHTML = d.date
            let ra = document.createElement("td")
            ra.innerHTML = d.ra
            let decl = document.createElement("td")
            decl.innerHTML = d.decl
            let offset = document.createElement("td")
            offset.innerHTML = d.offset
            let mag = document.createElement("td")
            mag.innerHTML = d.mag

            tr.append(name)
            tr.append(galaxy)
            tr.append(date)
            tr.append(ra)
            tr.append(decl)
            tr.append(offset)
            tr.append(mag)

            document.getElementById("table-supernovae").getElementsByTagName("tbody")[0].append(tr)

            //$("#table-supernovae").DataTable()
        }
        
        if(Object.values(data).length){
            $("#table-supernovae").removeClass("hidden")
        }
        
        $("#btn-extract-supernova").removeClass("hidden")
        

        $("#loading").removeClass("hidden").addClass("hidden")
    },
})

function extractSupernovas(){
    $.ajax({
        url: "/api/extract_sn/start",
        type: "GET",
        dataType: "json",
        success: data => {
            setInterval(reloadSupernovas, 1000)
        },
    });
    Notify("info", "L'extraction de nouvelles supernovas est en cours")
}

function reloadSupernovas(){
    $.ajax({
        url: "/api/extract_sn/progress",
        type: "GET",
        dataType: "json",
        success: data => {
            if(data["status"]=="ended"){
                location.href = "/supernovas?new=true"
            }
        },
    });
}

function detectSupernovas(){
    $.ajax({
        url: "/api/convert_sn?nb_containers=10",
        type: "GET",
        dataType: "json",
        success: data => {
            Notify(data.type, data.message)
        },
    });
}

function placeSupernovas(){
    $.ajax({
        url: "/api/active_sn",
        type: "GET",
        dataType: "json",
        success: data => {
            Notify(data.type, data.message)
        },
    });
}