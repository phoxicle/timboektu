$(function() {
	
	//$('a[href^="mailto"]').attr('rel', 'external');
	
	$('a[rel=external]').click(function(e) {
		window.open($(this).attr('href'));
		e.preventDefault();
	});
	
});