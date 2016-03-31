$(function() {
	$("button#add-user").on("click", function(event) {
		var data = $("form#add-user-form").serialize();
		var username = $("input#username").val();
		addUser(username, data, function(response) {
			$.notify("User created", "success");
			window.setTimeout(function() {
				window.location.reload();
			    }, 2000);
		    },
		    function(xhr, textStatus, errorThrown) {
			$.notify("Error: " + xhr.responseText, "error");
		    });
	    });
    });
