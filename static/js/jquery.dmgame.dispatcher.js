/**
 * Рассыльщик сообщений.
 * @author Mic, 2011
 */

(function($) {

	$.dmgame.dispatcher = {
		bind: function(event, callback) {
			$(document).bind(event, callback);
		},
		
		trigger: function(event, data) {
			$(document).trigger(event, data);
		}
	};

})(jQuery);
