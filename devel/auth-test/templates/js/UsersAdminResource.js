$(function() {
	var addUserSuccess = function(response) {
	    window.setTimeout(function() {
		    window.location.reload();
		}, 2000);
	};

	$("button#add-user").on("click", function(event) {
		var data = $("form#add-user-form").serialize();
		var username = $("input#username").val();
		addUser(username, data, addUserSuccess);
	    });
    });
