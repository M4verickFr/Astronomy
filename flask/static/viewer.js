let aladin;

A.init.then(() => {
    let url = new URL(location.href)
    let ra = url.searchParams.get("ra")
    let decl = url.searchParams.get("decl")

    let target = 'galactic center'
    let fov = 360
    if(ra && decl){
        target = ra + " " + decl
        fov = 1
    }

    aladin = A.aladin('#aladin-lite-div', { 
        cooFrame: 'galactic', 
        target: target, 
        showSimbadPointerControl: true, 
        fov: fov, 
        projection: "AIT", 
        cooFrame: 'equatorial', 
        showCooGridControl: true, 
        showSimbadPointerControl: true, 
        showCooGrid: true
    });

    // Set the base image layer to DSS2 colored
    aladin.setBaseImageLayer('P/DSS2/color');
    
    // Add a HiPS layer
    aladin.setOverlayImageLayer(aladin.createImageSurvey("Data", "Data", "http://localhost:81/data/hips/UNK.AUTH_P_HiPSID", "equatorial", 9, { imgFormat: "png" }));
    // aladin.setOverlayImageLayer(aladin.createImageSurvey('VTSS', 'VTSS', 'https://alasky.u-strasbg.fr/VTSS/Ha', 'galactic', 3, {imgFormat: 'png'}));
    aladin.getOverlayImageLayer().setAlpha(1.0);
    
    // Add a catalog
    // var hips = A.catalogHiPS('http://localhost:8000/DataHiPS', {onClick: 'showTable', name: 'Catalog'});
    // aladin.addCatalog(hips);
    
    
    $.ajax({
        url: "/api/sn?active=true",
        type: "GET",
        dataType: "json",
        success: data => {
            const cat = A.catalog({ color: 'red', onClick: 'showTable' });
            var originalSources = [];
            for (let d of data){
                originalSources.push(
                    A.marker(d.ra_degree, d.decl_degree, {popupTitle: d.name, popupDesc: d.galaxy}),
                );
            }
            cat.addSources(originalSources);
            aladin.addCatalog(cat);
        }
    })
    

});