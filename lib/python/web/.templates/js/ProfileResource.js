function buttonInit() {
    $("button#update-user").on("click", function(event) {
	var data = $("input#password").serialize();
	updateProfile(data, function(response) {
	    $.notify("User profile updated", "success");
	});
    });
}

$(function() {
    buttonInit();
});
