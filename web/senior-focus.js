// Rushy Panchal
// senior-focus.js
// Client-side library for my Senior Focus project

function initializeFocus() {
	// Main function
	socket.create();
	board.create(8, 8);
	resizeGameTiles();
	}

function resizeGameTiles() {
	// Resize all of the game tiles to fit all 8 inside the board
	$board = $("#board");
	var boardWidth = $board.width();
	var tileSize = boardWidth / 8;
	$('.board-tile').css('width', tileSize).css('height', tileSize);
	$board.css('margin-left', $(window).width() / 4); // NOT WORKING: attempt to move the board to center it exactly
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
	workingMove: [],
	create: function(height, width) {
		var board = this;
		var gameBoard = $("#board");
		for (h = 0; h < height; h++) {
			var row = document.createElement("div");
			row.className = "board-row";
			for (w = 0; w < width; w++) {
				var tile = document.createElement("div");
				tile.className = "board-tile";
				var tileData = tile.dataset;
				tileData["y"] = h;
				tileData["x"] = w;
				row.appendChild(tile);
				(function(t) { // this has to be an explicit function or otherwise, each .click event handler is the same
					$(t).click(function() {
						var $t = $(this);
						var location = [this.dataset.y, this.dataset.x];
						var locationString = location.toString();
						if ($t.hasClass("active")) {
							// Remove the current activation if already activated
							$t.removeClass("active");
							board.workingMove.forEach(function (elem, index) {
								if (elem.toString() == locationString) {
									board.workingMove.splice(index, 1);
									}
								});
							$t.empty();
							}
						else { // because it's not currently active, activate the tile
							$t.addClass("active");
							board.workingMove.push(location);
							var piece = document.createElement("p");
							piece.className = "game-piece black";
							$t.append(piece);
							}
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
		},
	submit: function() {
		// Submit the game move
		$('.board-tile').removeClass("active");
		console.log(this.workingMove);
		this.workingMove = [];
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
$(window).resize(resizeGameTiles);
