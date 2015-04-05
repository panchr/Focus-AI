// Rushy Panchal
// lib/focus.js

var express = require("express"),
	socketIO = require("socket.io"); // socket.io to communicate with client

var Socket = require("./socket"); // custom socket library to communicate with server

function focus(app, server, config) {
	// Prep the app for Focus-related deployments
	var focusRouter = express.Router();
	var clientSocket = socketIO(server);
	var serverSocket = new Socket({
		host: config.focus.host,
		port: config.focus.port
		}, console.log);

	focusRouter.get("/", function (req, res) {
		res.render("senior-focus.ejs");
		});

	app.use("/focus", focusRouter);

	clientSocket.on('connection', function (socket) {
		// using serverSocket, create a new game and then send back the game ID

		socket.on('move', function (move) {
			// proxy to the main server and give the proper response
			});
		socket.on('feedback', function (data) {
			// proxy to main server
			});
		socket.on('disconnect', function() {
			// tell the game server to end the game
			});
		});
	}

module.exports = focus;
