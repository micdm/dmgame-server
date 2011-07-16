/**
 * Рассыльщик сообщений.
 * @author Mic, 2011
 */

(function($) {

	var bind = function(event, callback) {
		$(document).bind(event, callback);
	};
	
	var trigger = function(event, data) {
		$(document).trigger(event, data);
	};
	
	var bind_to_incoming = function(type, callback) {
		bind('incoming.message', function(event, message_type, data) {
			if (type.join(':') == message_type.join(':')) {
				callback(data);
			}
		});
	};
	
	var trigger_outcoming = function(type, data) {
		trigger('outcoming.message', [type, data]);
	}
	
	$.dmgame.dispatcher = {
		bind: bind,
		trigger: trigger,
		bind_to_incoming: bind_to_incoming,
		trigger_outcoming: trigger_outcoming
	};

})(jQuery);
