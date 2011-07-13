/**
 * "Глупый" клиент, который просто выполняет последовательно действия.
 * @author Mic, 2011
 */

function dummyClient(swf_location, server) {

	var plain_queue = [];
	var evented_queue = {};
	
	function _buildPacket(namespace, type, data) {
		var packet = {code: namespace + ':' + type};
		if (data) {
			packet.data = data
		}
		return packet
	}
	
	function _doRequest(ws) {
		var msg = plain_queue.shift();
		if (msg) {
			console.log('sending message');
			ws.send($.toJSON(msg));
		} else {
			console.log('no messages left');
		}
	}
	
	function _doRequestAfterEvent(ws, event) {
		var msg = evented_queue[event];
		if (msg) {
			console.log('sending message');
			ws.send($.toJSON(msg));
			//delete evented_queue[event];
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
			var parsed = $.evalJSON(msg.data)
			_doRequestAfterEvent(ws, parsed.code);
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
			var packet = _buildPacket(namespace, type, data)
			plain_queue.push(packet);
		},
		
		on: function(event_namespace, event_type, namespace, type, data) {
			var packet = _buildPacket(namespace, type, data)
			evented_queue[event_namespace + ':' + event_type] = packet;
		},
		
		init: function() {
			_initWebsocket();
		} 
	};
}
