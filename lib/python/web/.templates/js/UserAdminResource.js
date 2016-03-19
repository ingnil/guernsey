$(function() {
	var deleteUserSuccess = function(response) {
	    window.setTimeout(function() {
		    window.location.replace("..");
		}, 2000);
	};

	$("button#delete-user").on("click", function(event) {
		var username = $("input#username").val();
		deleteUser(username, deleteUserSuccess);
	    });
    });
