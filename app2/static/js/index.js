var jwt;
var origin = window.location.origin;

/**
 * When log in button is pressed username and password fields are send to
 * database to verify authorized user. If verified user is presented with
 * navigation menu.
 */
$('#login').click(function() {
	fetch(origin + '/login', {
			method: 'post',
			headers: {
				"Content-type": "application/json"
			},
			body: JSON.stringify({
				"username": $('#username').val(),
				"password": $('#password').val()
			})
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			jwt = json;
			if (jwt['access_token']) {
				$('#login_field').hide();
				$('#choice').show();
			}
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 * When register button is pressed username and password fields are send to
 * database to verify authorized user. If verified user is presented with
 * navigation menu.
 */
$('#register').click(function() {
	fetch(origin + '/register', {
			method: 'post',
			headers: {
				"Content-type": "application/json"
			},
			body: JSON.stringify({
				"username": $('#username').val(),
				"password": $('#password').val()
			})
		})
		.then(function(response) {
			return response.json();
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 * When navigation option make request is clicked all other forms
 * are hidden and make request form is displayed.
 */
$('#nav_post_r').click(function() {
	$('form').hide();
	$('#post_request').show();
	populate_clients()
});

/**
 *  When navigation option get requests for client is clicked all
 *  other forms are hidden and client selection form is displayed.
 */
$('#nav_get_r').click(function() {
	$('form').hide();
	$('#get_request').show();
	populate_clients();
});

/**
 *  When navigation option get request by id is clicked all
 *  other forms are hidden and request by id form is displayed.
 */
$('#nav_get_r_id').click(function() {
	$('form').hide();
	$('#get_request_id').show();
});

/**
 *  When navigation option delete request by id is clicked all
 *  other forms are hidden and delete request by id form is displayed.
 */
$('#nav_del_r_id').click(function() {
	$('form').hide();
	$('#del_request_id').show();
});

/**
 *  When navigation option add client is clicked all
 *  other forms are hidden and add client form is displayed.
 */
$('#nav_post_c').click(function() {
	$('form').hide();
	$('#post_client').show();
});

/**
 *  When navigation option delete client is clicked all
 *  other forms are hidden and delete client form is displayed.
 */
$('#nav_del_c').click(function() {
	$('form').hide();
	$('#del_client').show();
});

/**
 * When submit request button is clicked all form data is sent as a request
 * to be stored. All fields must be filled in for a request to be made.
 * Otherwise a message is displayed indicating a field was left blank.
 */
$('#submit_request').click(function() {
	fetch(origin + '/request', {
			method: 'post',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			},
			body: JSON.stringify({
				"priority": $('#priority').val(),
				"target_date": $('#target_date').val(),
				"product_area": $('#product_area option:selected').text(),
				"client_name": $('#client_list option:selected').text(),
				"title": $('#title').val(),
				"description": $('#description').val()
			})
		})
		.then(function(response) {
			if (response.status === 201) {
				return response.json();
			} else {
				return {
					"message": "A field was left blank or a field was entered incorrectly!"
				}
			}
		})
		.then(function(json) {
			parse_requests([json])
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 *When find client requests button is clicked all requests for that
 * client will be displayed.
 */
$('#find_client_requests').click(function() {
	$.ajax({
		type: "GET",
		url: origin + '/client/' + $('#clients option:selected').text(),
		dataType: 'json',
		headers: {
			authorization: 'Bearer ' + jwt['access_token'],
			contentType: 'application/json'
		},
		contentType: 'application/json',
		success: function(data, textStatus, jQxhr) {
			var client_requests = data['requests'];
			parse_requests(client_requests);
		},
		error: function(jqXhr, textStatus, errorThrown) {
			console.log(errorThrown);
		}
	});
	return false;
});

/**
 * When the find request button is clicked if the request exists
 * it will be displayed, otherwise a message will be displayed
 * saying no request found.
 */
$('#find_request_id').click(function() {
	fetch(origin + '/request/' + $('#req_id').val(), {
			method: 'get',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			}
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			parse_requests([json])
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 * When the delete request button is pressed if the request was
 * deleted a message informing the user will be displayed, otherwise
 * a message will display informing the user the request wasn't found.
 */
$('#delete_request_id').click(function() {
	fetch(origin + '/request/' + $('#del_req_id').val(), {
			method: 'delete',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			}
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			parse_requests([json])
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 * When the add client button is clicked if the client already
 * exists a message will be displayed to that effect, otherwise
 * the client will be added and a message will display the client name
 * with their requests which is currently empty.
 */
$('#add_client_name').click(function() {
	fetch(origin + '/client/' + $('#client_name').val(), {
			method: 'post',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			}
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			parse_requests([json])
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 * When the delete client button is clicked if a client with that name
 * is found all their requests and that client will be deleted and a
 * message to that effect will be displayed. Otherwise it will display
 * a message saying the client wasn't found.
 */
$('#delete_client_name').click(function() {
	fetch(origin + '/client/' + $('#del_client_name').val(), {
			method: 'delete',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			}
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			parse_requests([json])
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
});

/**
 *The function populates the client lists of the make new request
 * form and get clients request form from currently existing clients.
 */
function populate_clients() {
	fetch(origin + '/clients', {
			method: 'get',
			headers: {
				"Content-type": "application/json",
				"authorization": 'Bearer ' + jwt['access_token']
			}
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			var clients = json.clients;
			$('#clients option').remove();
			$('#client_list option').remove();
			$.each(clients, function(key, value) {
				$('#clients')
					.append($("<option></option>")
						.attr("value", value)
						.text(value));
				$('#client_list')
					.append($("<option></option>")
						.attr("value", value)
						.text(value));
			});
		})
		.catch(function(error) {
			console.log('Request failed', error);
		});
	return false;
}

/**
 * The function parses the client request to display them as a message
 * for the user.
 * @param client_requests json object of client requests
 */
function parse_requests(client_requests) {
	$('#results').empty();
	if (!Array.isArray(client_requests) || !client_requests.length) {
  		// array does not exist, is not an array, or is empty
  		// ⇒ do not attempt to process array
		$('#results').append($("<p></p>").text('message: No Results'))
	}
	else {
		$.each(client_requests, function (k, v) {
			$.each(v, function (key, value) {
				$('#results')
					.append($("<p></p>")
						.text(key + ': ' + value));
			});
		});
	}
	$('#results').show();
}
