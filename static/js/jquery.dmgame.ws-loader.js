/**
 * WebSockets-загрузчик.
 * @author Mic, 2011
 */

(function($) {

	var ws = null;
	
	var onConnectionOpen = function() {
		$.dmgame.dispatcher.trigger('init');
	}

	var onConnectionClose = function() {
		$.dmgame.dispatcher.trigger('deinit');
	}

	var onMessage = function(message) {
		var packet = $.evalJSON(message.data);
		$.dmgame.dispatcher.trigger('incoming.message', [packet.code.split(':'), packet.data]);
	}
	
	var setup = function(address) {
		if (ws) {
			throw Error('loader already initialized');
		}
		ws = new WebSocket(address);
		ws.onopen = onConnectionOpen;
		ws.onclose = onConnectionClose;
		ws.onmessage = onMessage;
	}
	
	var listenToOutcoming = function() {
		$.dmgame.dispatcher.bind('outcoming.message', function(event, type, data) {
			var packet = {code: type.join(':')};
			if (data) {
				packet.data = data;
			}
			ws.send($.toJSON(packet));
		});
	}
	
	$.dmgame.wsLoader = function(swf_location, address) {
		WEB_SOCKET_SWF_LOCATION = swf_location;
		WEB_SOCKET_DEBUG = true;
		setup(address);
		listenToOutcoming();
	};

})(jQuery);
