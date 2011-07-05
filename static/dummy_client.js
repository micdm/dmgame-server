/**
 * "Глупый" клиент, который просто выполняет последовательно действия.
 * @author Mic, 2011
 */

function dummyClient(swf_location, server) {

	function _doRequest(ws, queue) {
		var msg = queue.shift();
		if (msg) {
			console.log('sending message');
			ws.send($.toJSON(msg));
		} else {
			console.log('no messages left');
		}
	}	
	
	function _initWebsocket(queue) {
		WEB_SOCKET_SWF_LOCATION = swf_location;
		WEB_SOCKET_DEBUG = true;

		var ws = new WebSocket(server);

		ws.onopen = function() {
			console.log('opened');
			_doRequest(ws, queue);
		};
		
		ws.onmessage = function(msg) {
			console.log('message received: ', msg);
			_doRequest(ws, queue);
		};
		
		ws.onclose = function() {
			console.log('closed');
		};
		
		ws.onerror = function() {
			console.log('error');
		};
	}

	return {
		init: function(queue) {
			_initWebsocket(queue);
		}
	};
}
