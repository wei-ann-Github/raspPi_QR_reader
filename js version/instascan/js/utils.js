/* Global variables */
var msg

/* Functions for querying the DB */
function askServer(id) {
	if (id == 'na')
		id = getElementById('enterSearchString').value
	var dataToSend = "?id=" + id;
	req.open("GET", "db.php" + dataToSend, true);
	req.onreadystatechange = handleServerResponse;
	req.send();
	document.getElementById('result').innerHTML = "Request Sent.";
}

function handleServerResponse() {
	if((req.readyState == 4) && (req.status == 200)) {
		var result = req.responseText;
		console.log(result)
		if (result == 2)
			msg = "Welcome Back!"
		else if (result == 1)
			msg = "We are expecting you!"
		else if (result == 0)
			msg = "Thank you for joining our breakout session!"
		document.getElementById('result').value = msg
	}
}

/* Functions to start the scanning. */
function startScan() {
	// The scanner starts
	let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
	scanner.addListener('scan', function (content) {
		askServer(content);
	});
	Instascan.Camera.getCameras().then(function (cameras) {
	if (cameras.length > 0) {
		scanner.start(cameras[0]);
	} else {
		console.error('No cameras found.');
	}
	}).catch(function (e) {
		console.error(e);
	});
	return
}

/* Function for modal */
function open_modal() {
	document.getElementById("modal-text").innerHTML = "Please wait."
}
