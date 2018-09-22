/* Global variables */
var lines = [];  // Used in processData
var idIndex;
var timeIndex;
var newLine;  // For recording walkins

/* Functions for querying the DB */
var req = new XMLHttpRequest();
var msg

function askServer(id) {
	if (id == 'na')
		id = getElementById('enterSearchString').value
	var dataToSend = "?id=" + id;
	req.open("GET", "db.php" + dataToSend, true);
	req.onreadystatechange = handleServerResponse;
	req.send();
	document.getElementById('result').innerHTML = "Request Sent.";
	alert("Hello " + id);
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
		document.getElementById('result').innerHTML = msg;
	}
}


/* Functions to start the scanning. */
// ToDo, when the file is uploaded, click the start button to start scanning
function startScan() {
	// The scanner starts
	let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
	scanner.addListener('scan', function (content) {
		//console.log(content);
		//welcomeMsg(content);
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
	// The id='fileUpload' and "howToStart" disappears. "Preview" Appears.
	document.getElementById("fileUpload").style.display = "none";
	document.getElementById("howToStart").style.display = "none";
	document.getElementById("uploadInstructions").style.display = "none";
	document.getElementById("startButton").style.display = "none";
	document.getElementById("preview").style.display = "inline";
	// "textbox" appears. This text box allows the user to type in this own EID.
	document.getElementById("textbox").style.display = "inline";
	// Word on the start button changes to stop.
	return
}

function welcomeMsg(searchString) {
	// Searches lines for the EID
	// In the header row, find the index of the value "Time"
	timeIndex = lines[0].indexOf('Time')
	if (timeIndex==-1)
		lines[0].push('Time')
		timeIndex = lines[0].indexOf('Time')
	for (i=1; i<lines.length; i++) {
		//If found
		if (lines[i][idIndex]==searchString) {
			// if registered
			if (lines[i][timeIndex])
				alert('Welcome back!')
			// else not registered
			else {
				// add check-in time to EID
				console.log(lines[i]);
				lines[i][timeIndex] = Date().toLocaleString();
				// save file

				// returns welcome message
				alert('Welcome! We are expecting you.')
				console.log(lines[i]);
			return
			}
		}
	}
	// if the for loop completes, then the EID is not found.
	// add the EID and check in time as a new line to the file
	newLine = [];
	newLine[idIndex] = searchString;
	newLine[timeIndex] = Date().toLocaleString();
	lines[lines.length] = newLine
	// save file

	// returns welcome message
	alert('Welcome ' + searchString + '!')
	for (i=1; i < lines.length; i++)
		console.log(lines[i])
}
