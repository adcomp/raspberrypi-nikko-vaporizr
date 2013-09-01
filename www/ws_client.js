var ws = null;

function connect() {
	var host = $("#host").val();
	ws = new WebSocket("ws://" + host + ":8888/piremote");

	ws.onmessage = function(evt) {
		// console.log(evt.data);
		if (evt.data) {
			var data = JSON.parse(evt.data);
			update(data);
		}
		else {
			$('.bt').css('background', '#333');
		}
	};

	ws.onclose = function(evt) {
		console.log("Connection close ..");
		$("#host").css("background", "#bd1143"); 
		$('#input').css('display', 'none')
		$('#output').css('display', 'none')
		$('#connect').show()
	};

	ws.onopen = function(evt) {
		console.log("WebSocket open ..")
		$("#host").css("background", "#7eb52b"); 
		$('#input').css('display', 'block')
		$('#output').css('display', 'block')
		$('#connect').hide()
	};
}

function update(data) {
	
	$('.bt').css('background', '#333');

	for (key in data) {
		// console.log(key + ' -> ' + data[key])

		if (data[key]) {
			$('#bt_' + key).css('background', '#159');
		}
		else {
			$('#bt_' + key).css('background', '#333');
		}
	}
}

