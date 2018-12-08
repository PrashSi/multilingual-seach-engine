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

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawPie);

function drawPie(p, neg, neu) {

	var data = google.visualization.arrayToDataTable([
	  ['Sentiment', 'Number of Tweets'],
	  ['Positive',      5],
	  ['Negative',      10],
	  ['Neutral',  		15],
	]);

	var options = {
	  title: 'Sentiment Analysis'
	};

	var chart = new google.visualization.PieChart(document.getElementById('piechart'));

	chart.draw(data, options);
	return p
};