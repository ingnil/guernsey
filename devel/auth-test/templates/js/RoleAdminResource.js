$(function() {
	var deleteRoleSuccess = function(response) {
	    window.setTimeout(function() {
		    window.location.replace("/role-admin/");
		}, 2000);
	};

	$("button#delete-role").on("click", function(event) {
		var name = $("input#name").val();
		deleteRole(name, deleteRoleSuccess);
	    });
    });
