/**
 * Модуль для работы с игровым залом.
 * @author Mic, 2011
 */

(function($) {

	$.dmgame.hall = function() {
		// После аутентификации шлем запрос на вход в зал:
		$.dmgame.dispatcher.bind('ok.auth', function() {
			$.dmgame.dispatcher.trigger_outcoming(['hall', 'enter']);
		});
		
		// После входа в зал встаем в очередь игроков:
		$.dmgame.dispatcher.bind_to_incoming(['hall', 'welcome'], function() {
			$.dmgame.dispatcher.trigger_outcoming(['hall', 'play']);
		});
		
		// Принимаем приглашение вступить в группу:
		$.dmgame.dispatcher.bind_to_incoming(['hall', 'party_invite'], function() {
			$.dmgame.dispatcher.trigger_outcoming(['hall', 'accept_invite']);
		});
	};

})(jQuery);
