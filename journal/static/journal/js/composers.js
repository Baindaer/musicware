$('#modalComposer').on('show.bs.modal', function(e) {
    let composer_id = $(e.relatedTarget).data('composer-id');
    let composer_name = $(e.relatedTarget).data('composer-name');
    let composer_period = $(e.relatedTarget).data('composer-period');
    if (composer_id) {
        $(e.currentTarget).find('input[name="composer_name"]').val(composer_name);
        $(e.currentTarget).find('input[name="composer_id"]').val(composer_id);
        $(e.currentTarget).find('select[name="composer_period"]').val(composer_period);
    } else {
        $(e.currentTarget).find('button[id="delete_btn"]').hide();
        $(e.currentTarget).find('input[name="composer_name"]').val('');
        $(e.currentTarget).find('input[name="composer_id"]').val('');
        $(e.currentTarget).find('input[name="composer_period"]').val('');
    }
});