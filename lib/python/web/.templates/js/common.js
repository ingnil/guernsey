/*
    Guernsey - Library to simplify creating REST web services using Python and Twisted
    Copyright (C) 2014 Magine Sweden AB
    Copyright (C) 2016 Ingemar Nilsson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function deleteIssue(issueId, successCallback, errorCallback) {
    $.ajax({
        type: "DELETE",
	url: "/issues/" + issueId + "/",
	success: successCallback,
	error: errorCallback
    });
}

function deleteAllIssues(callback) {
    $.ajax({
        type: "DELETE",
	url: "/issues/all/",
        success: callback
    });
}
