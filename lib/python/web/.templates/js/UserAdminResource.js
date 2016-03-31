function buttonInit() {
    $("button#delete-user").on("click", function(event) {
	$("button#delete-user").prop("disabled", true);
	$("div#dialog-confirm").dialog("open");
    });
    
    $("button#update-user").on("click", function(event) {
	var data = $("select#permissions, select#roles, input#password").serialize();
	var username = $("td#username").text();
	addUser(username, data, function(response) {
	    $.notify("User updated", "success");
	});
    });
}

function dialogInit() {
    $("div#dialog-confirm").dialog({
        autoOpen: false,
	resizable: false,
	modal: true,
	width: 400,
	buttons: {
	    "Delete": function() {
		var username = $("td#username").text();
		deleteUser(username,
			   function(response) {
			       $.notify("User deleted", "success");
			       window.setTimeout(function() {
				       window.location.replace("..");
				   }, 2000);
			   });
		$(this).dialog("close");
	    },
	    Cancel: function() {
		$(this).dialog("close");
		$("button#delete-user").prop("disabled", false);
	    }
	}
    });
}

$(function() {
    buttonInit();
    dialogInit();
});
