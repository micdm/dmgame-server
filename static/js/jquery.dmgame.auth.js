/**
 * Модуль аутентификации.
 * @author Mic, 2011
 */

(function($) {

	$.dmgame.auth = function() {
		// При инициализации шлем запрос на аутентификацию:
		$.dmgame.dispatcher.bind('init', function() {
			$.dmgame.dispatcher.trigger_outcoming(['auth', 'login'], {login: 'foo', password: 'bar'});
		});
		
		// Если вход успешно прошел, шлем сообщение:
		$.dmgame.dispatcher.bind_to_incoming(['auth', 'login_status'], function(data) {
			if (data.status == 'OK') {
				console.log('auth ok');
				$.dmgame.dispatcher.trigger('ok.auth');
			}
		});
	};

})(jQuery);
