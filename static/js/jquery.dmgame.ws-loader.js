/**
 * WebSockets-загрузчик.
 * @author Mic, 2011
 */

(function($) {

	var onConnectionOpen = function() {
		$.dmgame.dispatcher.trigger('active.loader');
	}

	var onConnectionClose = function() {
		$.dmgame.dispatcher.trigger('inactive.loader');
	}

	var onMessage = function(message) {
		var packet = $.evalJSON(message.data);
		$.dmgame.dispatcher.trigger('message.loader', packet);
	}
	
	$.dmgame.wsLoader = function(swf_location, address) {
		WEB_SOCKET_SWF_LOCATION = swf_location;
		WEB_SOCKET_DEBUG = true;

		var ws = new WebSocket(address);
		ws.onopen = onConnectionOpen;
		ws.onclose = onConnectionClose;
		ws.onmessage = onMessage;
	};

})(jQuery);
