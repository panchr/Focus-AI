// Rushy Panchal
// senior-focus.js
// Client-side library for my Senior Focus project

function initializeFocus() {
	// Main function
	socket.create();
	board.create(8, 8);
	}

function toggleInterface(elem) {
	// Toggle the element
	$elem = $(elem);
	if ($elem.css('display') == 'none') {
		$elem.slideDown();
		}
	else {
		$elem.slideUp();
		}
	}

var socket = {
	conn: null,
	create: function(settings) {
		// create the socket connection here
		}
	};

var board = {
	pieces: {},
	create: function(height, width) {
		var board = this;
		var gameBoard = $("#board");
		for (h = 0; h < height; h++) {
			var row = document.createElement("div");
			row.className = "board-row";
			for (w = 0; w < width; w++) {
				var tile = document.createElement("div");
				tile.className = "board-tile";
				row.appendChild(tile);
				(function(t) {
					$(t).click(function() {
						// $(".board-tile").removeClass("active");
						$(t).addClass("active");
						});
					}(tile));
				}
			gameBoard.append(row);
			gameBoard.append(document.createElement("br"));
			}
		this.init(height, width);
		},
	init: function(height, width) {
		// Initialize the game board
		return null;
		}
	}

var players = {
	allPlayers: {},
	toggleDown: 'ion-ios7-arrow-thin-up',
	toggleUp: 'ion-ios7-arrow-thin-down',
	toggle: function() {
		// Toggle the list of players
		var players = this;
		$("#online-players-list").slideToggle(function() {
			$toggler = $("#player-list-toggler");
			if ($toggler.hasClass(players.toggleUp)) {
				$toggler.removeClass(players.toggleUp).addClass(players.toggleDown);
				}
			else {
				$toggler.removeClass(players.toggleDown).addClass(players.toggleUp);
				}
			});
		},
	add: function(name) {
		// Add to the list of players
		var player = document.createElement("li");
		player.innerHTML = name;
		player.className = "online-player";
		$("#online-players-list").append(player);
		this.allPlayers[name] = player;
		},
	remove: function(name) {
		// Remove from the list of players
		if (name in this.allPlayers) {
			$(this.allPlayers[name]).remove();
			delete this.allPlayers[name];
			}
		}
	};

$(document).ready(initializeFocus);
