$(function() {
	var addRoleSuccess = function(response) {
	    window.setTimeout(function() {
		    window.location.reload();
		}, 2000);
	};

	$("button#add-role").on("click", function(event) {
		var data = $("select#permissions").serialize();
		var name = $("input#name").val();
		addRole(name, data, addRoleSuccess);
	    });
    });
