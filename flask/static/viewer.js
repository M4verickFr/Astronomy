A.init.then(() => {
    const aladin = A.aladin('#aladin-lite-div', { 
        cooFrame: 'galactic', 
        fov: 110, 
        target: 'galactic center', 
        showSimbadPointerControl: true, 
        fov: 360, 
        projection: "AIT", 
        cooFrame: 'equatorial', 
        showCooGridControl: true, 
        showSimbadPointerControl: true, 
        showCooGrid: true 
    });

    // Set the base image layer to DSS2 colored
    aladin.setBaseImageLayer('P/DSS2/color');
    
    // Add a HiPS layer
    // aladin.setOverlayImageLayer(aladin.createImageSurvey("Data", "Data", "data/DataHiPS", "equatorial", 9, { imgFormat: "png" }));
    // aladin.getOverlayImageLayer().setAlpha(1.0);
    
    // Add a catalog
    // var hips = A.catalogHiPS('http://localhost:8000/DataHiPS', {onClick: 'showTable', name: 'Catalog'});
    // aladin.addCatalog(hips);
    
    const cat = A.catalog({ color: 'red', onClick: 'showTable' });
    const originalSources = [
        A.source(204.971666667, -31.67083333, { name: 'S1' }),
        A.source(56.1, -44.66, { name: 'S2' }),
    ];
    
    cat.addSources(originalSources);
    
    aladin.addCatalog(cat);

});