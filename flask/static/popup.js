/**
 * Envoie une notification à l'utilisateur
 * @param {*} type Le type du message (succes, info, warning, danger)
 * @param {*} message Contenu du message
 * @param {*} delay Delay en millisecondes
 */
function Notify(type, message, delay = 3000) {
    switch(type){
        case "success":
            icon = "glyphicon glyphicon-ok"
            title = "<strong>Success</strong>"
            break
        case "info":
            icon = "glyphicon glyphicon-info-sign"
            title = "<strong>Information</strong>"
            break
        case "warning":
            icon = "glyphicon glyphicon-warning-sign"
            title = "<strong>Warning</strong>"
            break
        case "danger":
            icon = "glyphicon glyphicon-remove-sign"
            title = "<strong>Danger</strong>"
            break
        default:
            icon = "glyphicon glyphicon-warning-sign"
            title = "<strong>Default</strong>"
            break
    };
    
    $.notify({
        // options
        title: title,
        message: message,
        icon: icon,
    },{
        // settings
        element: 'body',
        //position: null,
        type: type,
        //allow_dismiss: true,
        //newest_on_top: false,
        showProgressbar: false,
        placement: {
            from: "bottom",
            align: "right"
        },
        offset: 20,
        spacing: 10,
        z_index: 1031,
        delay: delay,
        timer: 1000,
        url_target: '_blank',
        mouse_over: null,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutRight'
        },
        onShow: null,
        onShown: null,
        onClose: null,
        onClosed: null,
        icon_type: 'class',
    });
}
