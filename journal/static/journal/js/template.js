$.fn.difficulty_tag = function() {
    return $(this).each(function() {
        let diff = parseInt($(this).data("difficulty"));
        if (diff <= 2) {
            $(this).attr("style", "background-color: #cb4b16;");
        } else if (diff <= 4) {
            $(this).attr("style", "background-color: #839496;");
        } else if (diff <= 6) {
            $(this).attr("style", "background-color: #b58900;");
        } else if (diff <= 8) {
            $(this).attr("style", "background-color: #6c71c4;");
        } else if (diff <= 10) {
            $(this).attr("style", "background-color: #268bd2;");
        } else {
            $(this).attr("style", "background-color: #002b36;");
        }
    });
};
$('.kbd_difficulty').difficulty_tag();

$.fn.stars = function() {
    return $(this).each(function() {
        let rating = $(this).data("rating");
        let numStars = $(this).data("numStars");
        let fullStar = new Array(Math.floor(rating + 1)).join('<i class="fa fa-star"></i>');
        let halfStar = ((rating%1) !== 0) ? '<i class="fa fa-star-half-empty"></i>': '';
        let noStar = new Array(Math.floor(numStars + 1 - rating)).join('<i class="fa fa-star-o"></i>');
        $(this).html(fullStar + halfStar + noStar);
    });
};
$('.stars').stars();