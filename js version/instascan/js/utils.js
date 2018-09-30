/* Global variables */
var msg

/* Functions for querying the DB */
function askServer(id) {
	if (id == "null")  // This is for getting the id when the Enter button is pressed.
		id = document.getElementById('enterSearchString').value
	if (id.length == 0)
		return
	document.getElementById('enterSearchString').value = ""
	var dataToSend = "?id=" + id;
	console.log(dataToSend);
	req.open("GET", "db.php" + dataToSend, true);
	req.onreadystatechange = handleServerResponse;
	req.send();
}

function handleServerResponse() {
	if((req.readyState == 4) && (req.status == 200)) {
		var q_result = req.responseText;
		result = JSON.parse(q_result)[0]
		name = JSON.parse(q_result)[1]
		if (name=="null")	
			name = ""
		else
			name = " " + name
		if (result == 2)
			//document.getElementById("modal-text").innerHTML = "Welcome Back!"
			msg = "Welcome Back!"
		else if (result == 1)
			//document.getElementById("modal-text").innerHTML = "We are expecting you!"
			msg = "Hi" + name + "!"
		else if (result == 0)
			//document.getElementById("modal-text").innerHTML = "Thank you for joining our breakout session!"
			msg = "Thank you for joining our breakout session!"
		document.getElementById('p1').innerHTML = msg;
	}
}

/* Functions to start the scanning. */
function startScan() {
	// The scanner starts
	let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
	scanner.addListener('scan', function (content) {
		openModal()
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
