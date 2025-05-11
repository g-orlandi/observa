function onOpenEditEndpoint(event) {
    let dialog_edit = new HtmxForms.Dialog({
        dialog_selector: '#dialog_generic',
        html: 'Loading in progress...',
        width: '600px',
        min_height: '200px',
        enable_trace: true,
        callback: function(event_name, dialog, params) {
            if (event_name == 'submitted') {
                HtmxForms.reload_page(show_layer = false);
            }
        },
    });
    dialog_edit.open(event);
}

function onOpenDeleteEndpoint(event) {
    let dialog_delete = new HtmxForms.Dialog({
        dialog_selector: '#dialog_generic',
        html: 'Loading in progress...',
        width: '600px',
        min_height: '200px',
        button_save_label: "Delete",
        enable_trace: true,
        callback: function(event_name, dialog, params) {
            if (event_name == 'submitted') {
                HtmxForms.reload_page(show_layer = false);
            }
        },
    });
    dialog_delete.open(event);
}