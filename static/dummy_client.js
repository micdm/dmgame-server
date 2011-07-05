/**
 * "Глупый" клиент, который просто выполняет последовательно действия.
 * @author Mic, 2011
 */

function dummyClient(swf_location, server) {

	var queue = [];
	
	function _doRequest(ws) {
		var msg = queue.shift();
		if (msg) {
			console.log('sending message');
			ws.send($.toJSON(msg));
		} else {
			console.log('no messages left');
		}
	}	
	
	function _initWebsocket() {
		WEB_SOCKET_SWF_LOCATION = swf_location;
		WEB_SOCKET_DEBUG = true;

		var ws = new WebSocket(server);

		ws.onopen = function() {
			console.log('opened');
			_doRequest(ws);
		};
		
		ws.onmessage = function(msg) {
			console.log('message received: ', msg);
			_doRequest(ws);
		};
		
		ws.onclose = function() {
			console.log('closed');
		};
		
		ws.onerror = function() {
			console.log('error');
		};
	}

	return {
		addToQueue: function(namespace, type, data) {
			var packet = {c: namespace + ':' + type};
			if (data) {
				packet.data = data
			}
			queue.push(packet);
		},
		
		init: function() {
			_initWebsocket();
		} 
	};
}
