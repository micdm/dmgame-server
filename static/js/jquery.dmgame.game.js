/**
 * Игровой модуль.
 * @author Mic, 2011
 */

(function($) {

	var _container = null;

	var _id = null;
	var _members = null;
	
	var addMember = function(id) {
		_members[id] = {id: id};
		var title = (id == _id) ? 'Вы' : 'Игрок №' + id;
		_container.append('<div id="member' + id + '" class="member_area"><h2>' + title + '</h2></div>');
	}

	var setMemberTurning = function(id) {
		_container.find('.member_area').removeClass('now_turning');
		_container.find('#member' + id).addClass('now_turning');
		if (id == _id) {
			var more_button = $('<input type="button" value="Ещё карту">');
			more_button.click(function() {
				$.dmgame.dispatcher.trigger_outcoming(['game', 'turn'], {type: 'one_more_card'});
			});
			var enough_button = $('<input type="button" value="Достаточно">');
			enough_button.click(function() {
				$.dmgame.dispatcher.trigger_outcoming(['game', 'turn'], {type: 'cards_enough'});
			});
			_container.append($('<div id="controls"></div>').append(more_button).append(enough_button));
		} else {
			_container.find('#controls').remove();
		}
	}
	
	var setMemberResult = function(id, result) {
		var container = _container.find('#member' + id);
		if (result == 'win') {
			container.append('<div class="result win">Выигрыш</div>');
		}
		if (result == 'defeat') {
			container.append('<div class="result defeat">Проигрыш</div>');
		}
	}
	
	var getCardRow = function(suit) {
		var suits = ['♣', '♦', '♥', '♠'];
		return $.inArray(suit, suits);
	}
	
	var giveCardToMember = function(id, card) {
		if (card) {
			var col = card.rank - 1;
			var row = getCardRow(card.suit);
		} else {
			var col = 2;
			var row = 4;
		}
		var left = col * -80;
		var top = row * -116;
		_container.find('#member' + id).append('<div class="card" style="background-position: ' + left + 'px ' + top + 'px"></div>');
	}
	
	var removeMemberCards = function(id) {
		_container.find('#member' + id + ' .card').remove();
	}
	
	var setHandValue = function(id, value) {
		var title = _container.find('#member' + id + ' h2');
		var container = title.find('span');
		if (container.size()) {
			container.text('(' + value + ')');
		} else {
			title.append('<span>(' + value + ')</span>');
		}
	}
	
	var listenToGameStarted = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'game_started'], function(data) {
			_container.empty();
			_id = data.id;
			_members = {};
			for (var i in data.members) {
				addMember(data.members[i]);
			}
		});
	}

	var listenToMemberTurning = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'member_turning'], function(data) {
			setMemberTurning(data.id);
		});
	}
	
	var listenToResultsAvailable = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'results_available'], function(data) {
			for (var i in data) {
				var member = data[i];
				setMemberResult(member.id, member.result);
			}
		});
	}
	
	var listenToGameEnded = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'game_ended'], function(data) {
			_container.find('#controls').remove();
		});
	}
	
	var listenToGivingCards = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'giving_cards'], function(data) {
			if (data.count) {
				for (var i = 0; i < data.count; i += 1) {
					giveCardToMember(data.id);
				}
			} else {
				for (var i in data.cards) {
					giveCardToMember(data.id, data.cards[i]);
				}
			}
		});
	}
	
	var listenToOpeningCards = function() {
		$.dmgame.dispatcher.bind_to_incoming(['game', 'opening_cards'], function(data) {
			for (var i in data) {
				var member = data[i];
				removeMemberCards(member.id);
				for (var j in member.cards) {
					var card = member.cards[j];
					giveCardToMember(member.id, card);
				}
			}
		});
	}
	
	var listenToSetHandValue = function() {
		$.dmgame.dispatcher.bind_to_incoming(['a_la_21', 'set_hand_value'], function(data) {
			setHandValue(data.id, data.value);
		});
	}
	
	$.dmgame.game = function(container) {
		_container = container;
		listenToGameStarted();
		listenToMemberTurning();
		listenToResultsAvailable();
		listenToGameEnded();
		listenToGivingCards();
		listenToOpeningCards();
		listenToSetHandValue();
	};

})(jQuery);
