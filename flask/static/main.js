const showEvents = ['mouseenter', 'focus'];
const hideEvents = ['mouseleave', 'blur'];

function show(popper, popperInstance) {
    // Make the tooltip visible
    popper.classList.remove('d-none');
    
    // Enable the event listeners
    popperInstance.setOptions((options) => ({
        ...options,
        modifiers: [
            ...options.modifiers,
            { name: 'eventListeners', enabled: true },
        ],
    }));
    
    // Update its position
    popperInstance.update();
}

function hide(popper, popperInstance) {
    // Hide the tooltip
    popper.classList.add('d-none');
    
    // Disable the event listeners
    popperInstance.setOptions((options) => ({
        ...options,
        modifiers: [
            ...options.modifiers,
            { name: 'eventListeners', enabled: false },
        ],
    }));
}

document.addEventListener('DOMContentLoaded', event => { 
    let creators = document.querySelectorAll("footer span");
    
    for(let creator of creators) {
        // Create the popper element
        const popper = document.createElement('div');
        popper.innerHTML = creator.title;
        popper.classList.add('popper');
        
        const arrow = document.createElement('div');
        arrow.classList.add('arrow');
        arrow.setAttribute('data-popper-arrow', '');
        
        popper.appendChild(arrow)
        document.body.appendChild(popper);
        
        const popperInstance = Popper.createPopper(creator, popper, {
            placement: 'top',
            modifiers: [
                {
                    name: 'offset',
                    options: {
                        offset: [0, 8],
                    },
                },
            ],
        });
        
        showEvents.forEach((event) => {
            creator.addEventListener(event, () => show(popper, popperInstance));
        });
        
        hideEvents.forEach((event) => {
            creator.addEventListener(event, () => hide(popper, popperInstance));
        });

        hide(popper, popperInstance);
        creator.title = '';
    }


    
    

    

    
    
    
    
    
    
    
    
    
    
    
    
});

