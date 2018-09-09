$('#modalPracticeItem').on('show.bs.modal', function(e) {
    let item_id = $(e.relatedTarget).data('item-id');
    let item_name = $(e.relatedTarget).data('item-name');
    let item_composer = $(e.relatedTarget).data('item-composer');
    let item_difficulty = $(e.relatedTarget).data('item-difficulty');
    let item_self_appraisal = $(e.relatedTarget).data('item-self_appraisal');
    let item_type = $(e.relatedTarget).data('item-type');
    let item_date = $(e.relatedTarget).data('item-date');
    let date = new Date();
      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      if (month < 10)
        month = "0" + month;
      if (day < 10)
        day = "0" + day;
      let today = year + "-" + month + "-" + day;
    console.log(item_date);
    if (item_id) {
        $(e.currentTarget).find('input[name="item_name"]').val(item_name);
        $(e.currentTarget).find('input[name="item_id"]').val(item_id);
        $(e.currentTarget).find('select[name="item_composer"]').val(item_composer);
        $(e.currentTarget).find('input[name="item_difficulty"]').val(item_difficulty);
        $(e.currentTarget).find('input[name="item_self_appraisal"]').val(item_self_appraisal);
        $(e.currentTarget).find('select[name="item_type"]').val(item_type);
        $(e.currentTarget).find('input[name="item_date"]').val(item_date);
    } else {
        $(e.currentTarget).find('button[id="delete_btn"]').hide();
        $(e.currentTarget).find('input[name="item_name"]').val('');
        $(e.currentTarget).find('input[name="item_id"]').val('');
        $(e.currentTarget).find('select[name="item_composer"]').val('');
        $(e.currentTarget).find('input[name="item_difficulty"]').val('');
        $(e.currentTarget).find('input[name="item_self_appraisal"]').val('');
        $(e.currentTarget).find('select[name="item_type"]').val('');
        $(e.currentTarget).find('input[name="item_date"]').val(today);
    }
});