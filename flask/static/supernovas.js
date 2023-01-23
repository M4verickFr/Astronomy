// Make ajax request to api to load all supernova in database and create a boostrap table
$.ajax({
    url: "/api/sn",
    type: "GET",
    dataType: "json",
    success: data => {
        //console.log(data)

        // Generate stats

        let sn_stats = document.querySelector(".stats")
        sn_stats.style.height = '5px';

        let sn_active = document.querySelector(".sn_active");
        let sn_inactive = document.querySelector(".sn_inactive");
        let sn_processing = document.querySelector(".sn_processing");

        sn_active.style.width = `${data['sn_active']*100}%`
        sn_inactive.style.width = `${data['sn_inactive']*100}%`
        sn_processing.style.width = `${data['sn_processing']*100}%`

        sn_active.style.background = `green`
        sn_inactive.style.background = `red`
        sn_processing.style.background = `darkorange`

        // Generate table
        for (let d of data['t_sn']){
            let tr = document.createElement("tr")
            tr.onclick = function(e){
                if(!e.target.classList.contains("icon-redirect") &&  !e.target.classList.contains("blue-icon")){
                    location.href="./viewer?ra=" + d.ra_degree + "&decl=" + d.decl_degree
                }
                
            }
            let status = document.createElement("td")
            let point = document.createElement("span")
            point.classList.add("dot")
            status.append(point)

            if(d.activationDate){
                point.classList.add("bg-green")
            } else if(d.processingStartDate){
                point.classList.add("bg-orange")
            } else {
                point.classList.add("bg-red")
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
            let source = document.createElement("td")
            let a = document.createElement("a")
            a.href = d.url + "&format=gif"
            a.target="_blank";
            let i = document.createElement("i")
            i.classList.add("fa-regular", "fa-image", "blue-icon")
            a.append(i)
            source.append(a)
            source.classList.add("icon-redirect")

            tr.append(status)
            tr.append(name)
            tr.append(galaxy)
            tr.append(date)
            tr.append(ra)
            tr.append(decl)
            tr.append(offset)
            tr.append(mag)
            tr.append(source)

            document.getElementById("table-supernovae").getElementsByTagName("tbody")[0].append(tr)
        }
        
        if(Object.values(data).length){
            $("#table-supernovae").removeClass("hidden")
        }
        
        $("#btn-extract-supernova").removeClass("hidden")
        

        $("#loading").removeClass("hidden").addClass("hidden")
    },
})

/**
 * Extraction of supernovas
 */
function extractSupernovas(){
    $.ajax({
        url: "/api/extract_sn/start",
        type: "GET",
        dataType: "json",
        success: data => {
            Notify(data.type, data.message);
            if (data.type === 'info') {
                let interval = setInterval(() => {
                    $.ajax({
                        url: "/api/extract_sn/pid",
                        type: "GET",
                        dataType: "json",
                        success: data => {
                            if(typeof data["pid"] === 'undefined'){
                                clearInterval(interval);
                                location.href = "/supernovas?notify=supernovas_extracted"
                            }
                        },
                    });
                }, 1000);
            }
        },
    });
}

/**
 * Detect supernovas in images
 */
function detectSupernovas(){
    $.ajax({
        url: "/api/convert_sn/start?nb_containers=10",
        type: "GET",
        dataType: "json",
        success: data => {
            Notify(data.type, data.message)
            if (data.status === 'startImageBuilding') {
                let interval = setInterval(() => {
                    $.ajax({
                        url: "/api/convert_sn/pid",
                        type: "GET",
                        dataType: "json",
                        success: data => {
                            if(typeof data["pid"] === 'undefined'){
                                clearInterval(interval);
                                Notify("info", "The image has been built, start detection")
                                detectSupernovas()
                            }
                        },
                    });
                }, 1000);
            }
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