function buttonInit() {
    $("button#delete-role").on("click", function(event) {
        var name = $("input#name").val();
	$("button#delete-role").prop("disabled", true);
	$("div#dialog-confirm").dialog("open");
    });
    
    $("button#update-role").on("click", function(event) {
	var data = $("select#permissions, select#subroles").serialize();
	var name = $("input#name").val();
	addRole(name, data, function(response) {
	    $.notify("Role updated", "success");
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
		var name = $("input#name").val();
		deleteRole(name,
			   function(response) {
			       $.notify("Role deleted", "success");
			       window.setTimeout(function() {
				       window.location.replace("..");
				   }, 2000);
			   });
		$(this).dialog("close");
	    },
	    Cancel: function() {
		$(this).dialog("close");
		$("button#delete-role").prop("disabled", false);
	    }
	}
    });
}


$(function() {
    buttonInit();
    dialogInit();
});
