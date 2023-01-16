// Make ajax request to api to load all supernova in database and create a boostrap table

// TODO - make ajax request to api to load all supernovas in database
$.ajax({
    url: "/api/sn",
    type: "GET",
    dataType: "json",
    success: data => {
        //console.log(data)
        for (let d of data){
            let tr = document.createElement("tr")
            tr.onclick = function(){
                location.href="./viewer"
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

            $("#table-supernovae").removeClass("hidden")
            $("#loading").removeClass("hidden").addClass("hidden")

        }
    },
})