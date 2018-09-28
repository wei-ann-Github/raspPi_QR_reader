/* Global variables */
var lines = [];  // Used in processData
var idIndex;
var timeIndex;
var newLine;  // For recording walkins

/* For uploading CSV file */
function Upload() {
	var fileUpload = document.getElementById("fileUpload");
	var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
	if (regex.test(fileUpload.value.toLowerCase())) {
		if (typeof (FileReader) != "undefined") {
		var reader = new FileReader();
		reader.onload = function (e) {
			var table = document.createElement("table");
			var rows = e.target.result.split("\n");
			for (var i = 0; i < rows.length; i++) {
				var row = table.insertRow(-1);
				var cells = rows[i].split(",");
				for (var j = 0; j < cells.length; j++) {
					var cell = row.insertCell(-1);
					cell.innerHTML = cells[j];
				}
			}
			var dvCSV = document.getElementById("dvCSV");
			dvCSV.innerHTML = "";
			dvCSV.appendChild(table);
		}
		reader.readAsText(fileUpload.files[0]);
	} else {
		alert("This browser does not support HTML5.");
		}
	} else {
	alert("Please upload a valid CSV file.");
	}
}

/* Functions to read the files. */
function handleFiles(files) {
  // Check for the various File API support.
  if (window.FileReader) {
	  // FileReader are supported.
	  getAsText(files[0]);
	  console.log('files: ' + files[0])
  } else {
	  alert('FileReader are not supported in this browser.');
  }
}

function getAsText(fileToRead) {
  var reader = new FileReader();
  // Read file into memory as UTF-8      
  reader.readAsText(fileToRead);
  // Handle errors load
  reader.onload = loadHandler;
  reader.onerror = errorHandler;
}

function loadHandler(event) {
  var csv = event.target.result;
  processData(csv);
}

function processData(csv) {
	// requirement of the file.
	// It must contain the column name 'EID'
	var allTextLines = csv.split(/\r\n|\n/);
	for (var i=0; i<allTextLines.length; i++) {
		var data = allTextLines[i].split(',');
		if (i==0)
			idIndex = data.indexOf('EID')
		var tarr = [];
		for (var j=0; j<data.length; j++) {
			tarr.push(data[j]);
		}
		lines.push(tarr);
		console.log(tarr);
	}
	console.log(lines);
	if (lines.length<=1)
		alert("The file does not contain any data.")
}

function errorHandler(evt) {
  if(evt.target.error.name == "NotReadableError") {
	  alert("Canno't read file !");
  }
}

function saveCSV() {
	
}

/* Functions to start the scanning. */
// ToDo, when the file is uploaded, click the start button to start scanning
function startScan() {
	alert("Hello!");
	// If there are no data in lines, bring alert message.
	console.log("lines.length " + lines.length)
	if (lines.length<=1) {
		alert("No data was uploaded. Please upload another file.")
		return
	}
	// The scanner starts
	let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
	scanner.addListener('scan', function (content) {
	//console.log(content);
	welcomeMsg(content);
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

/* Functions for entering the EID manually */
function findName() {
	var searchString = document.getElementById("enterSearchString").value.trim().toLowerCase();
	document.getElementById("enterSearchString").value = "";
	// call function to search and record the information entered, and return a message.
	// the function also increase the count of elementID "enterSearchString"
	console.log("In findName(): " + searchString);
}

function validate(e) {
    var text = e.target.value.trim().toLowerCase();
    //validation of the input...
	console.log(text + " isEntered.");
}