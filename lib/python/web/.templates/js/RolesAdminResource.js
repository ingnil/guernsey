$(function() {
	var addRoleSuccess = function(response) {
	    $.notify("Role created", "success");
	    window.setTimeout(function() {
		    window.location.reload();
		}, 2000);
	};

	$("button#add-role").on("click", function(event) {
		var data = $("select#permissions, select#subroles").serialize();
		var name = $("input#name").val();
		addRole(name, data, addRoleSuccess);
	    });
    });
