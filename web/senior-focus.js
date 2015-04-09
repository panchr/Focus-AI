// Rushy Panchal
// senior-focus.js
// Client-side library for my Senior Focus project

function initializeFocus() {
	// Main function
	var socket = createSocketConnection();
	board.create(8, 8);
	}

function createSocketConnection() {
	// Create the main socket connection
	return null; // not yet implemented
	}

var board = {
	pieces: {},
	create: function(height, width) {
		var gameBoard = $("#board");
		for (h = 0; h < height; h++) {
			var row = document.createElement("div");
			row.className = "board-row";
			for (w = 0; w < width; w++) {
				var tile = document.createElement("div");
				tile.className = "board-tile";
				row.appendChild(tile);
				}
			gameBoard.append(row);
			gameBoard.append(document.createElement("br"));
			}
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
