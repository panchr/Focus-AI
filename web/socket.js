// Rushy Panchal
// web/lib/socket.js

var util = require("util"),
	EventEmitter = require("events").EventEmitter;

var zmq = require("zmq"),
	short_id = require("shortid").generate,
	_ = require("underscore");

function Socket(config, log) {
	// Creates a new socket connection
	this.config = _.extend({
		host: '127.0.0.1',
		port: 7337,
		retryWait: 1000,
		intervalTime: 200,
		}, config);
	this.waiting = 0;
	this.socketPath = "tcp://" + this.config.host + ":" + this.config.port;
	this.connection = zmq.socket('req');
	this.logger = log;
	}

util.inherits(Socket, EventEmitter);

Socket.prototype.connect = function() {
	// Connect to the socket
	var socket = this;
	this.connection.connect(this.socketPath);
	this.logger.info("Connected to: " + this.socketPath);
	this.connection.on("message", function (data) {
		socket.waiting--;
		var data = JSON.parse(data);
		socket.emit("data-" + data.msg_id, data);
		});
	return this;
	}

Socket.prototype.send = function(data) {
	// Send a message to the socket
	var msg_id = short_id();
	this.waiting++;
	data.msg_id = msg_id;
	this.connection.send(JSON.stringify(data));
	return msg_id;
	}

Socket.prototype.close = function() {
	// Close the socket connection
	this.connection.send("SOCKET_END"); // modified ZMQ-protocol message for a closed socket
	try {
		this.connection.close();
		}
	catch (e) {
		// do nothing, because the error was that the socket is already closed
		}
	this.logger.info("Disconnected from: " + this.socketPath);
	return this;
	}

Socket.prototype.response = function(id, callback) {
	// Wrapper for Socket.on(data-id)
	var clearSocket = setTimeout(function() {
		callback({
			req_id: id,
			response: {
				type: 504,
				status: "Gateway Timeout"
				}
			});
		}, 10000); // timeout after 10 seconds of no response
	return this.once('data-' + id, function(data) {
		clearTimeout(clearSocket);
		callback(data);
		});
	}

module.exports = Socket;
