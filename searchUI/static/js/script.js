$(".dropdown-menu li a").click(function(){
var selText = $(this).text();
$(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});

$('#myTab a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});

$(function () {
$('#myTab a:first').tab('show');
});


var monkeyList = new List('test-list', {
  valueNames: ['tweet_item'],
  page: 30,
  pagination: true
});