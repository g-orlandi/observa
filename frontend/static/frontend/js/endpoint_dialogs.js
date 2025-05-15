function onOpenDialog(event, button_save_label) {
    let dialog_obj = new HtmxForms.Dialog({
        dialog_selector: '#dialog_generic',
        html: 'Loading in progress...',
        button_save_label: button_save_label,
        width: '600px',
        min_height: '200px',
        enable_trace: true,
        callback: function(event_name, dialog, params) {
            if (event_name == 'submitted') {
                HtmxForms.reload_page(show_layer = false);
            }
        },
    });
    dialog_obj.open(event);
}