function addRole(name, data, successCb, errorCb) {
    $.ajax({
	type: "PUT",
	url: "/role-admin/" + name + "/",
	success: successCb,
	error: errorCb,
	data: data
    });
}

function deleteRole(name, successCb, errorCb) {
    $.ajax({
	type: "DELETE",
	url: "/role-admin/" + name + "/",
	success: successCb,
	error: errorCb
    });
}

function addUser(username, data, successCb, errorCb) {
    $.ajax({
	type: "PUT",
	url: "/user-admin/" + username + "/",
	success: successCb,
	error: errorCb,
	data: data
    });
}

function deleteUser(username, successCb, errorCb) {
    $.ajax({
	type: "DELETE",
	url: "/user-admin/" + username + "/",
	success: successCb,
	error: errorCb
    });
}


