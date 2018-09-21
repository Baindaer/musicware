$('#modalSession').on('show.bs.modal', function(e) {
    let comments = $(e.relatedTarget).data('item-data');
    if (comments && comments !== 'False') {
        comments = comments.replace(/'/g, '"');
        comments = JSON.parse(comments);
        let comm_html = '';
        for (let comm in comments) {
            comm_html += '<small class="text-muted"><i class="fa fa-asterisk pretext"></i>' + comments[comm] + '</small> <br/>'
        }
        $(e.currentTarget).find('div[id="comments"]').html(comm_html);
    }
    else {
        $(e.currentTarget).find('div[id="comments"]').html('<p>No comentary found fot this season</p>');
    }
});