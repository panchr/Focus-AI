## Web Development

I knew the easiest way for random people to access my game and play against my AI was if it was based online.
So, I decided to host the game and AI on my website.

### Web Design
Developing the actual interface was fairly straightforward once I fixed small graphical issues. However, I did run into one major problem, which was connecting the frontend webpage with the backend web service.

### Backend Connection
I used something called Socket.IO to handle WebSocket connections for me. This made it fairly simple to connect the frontend and the backend.

### IPC
However, my main website backend is created in `Node.js`, whereas my AI backend is created in `Python`.
I needed some way to connect the two, I decided to use IPC (Inter-process communication) software to accomplish this. After researching a few different types, I settled on `ZMQ`, which looked to be the simplest.

### Concurrent Connections
WebSockets allow for multiple connections at once. In addition, the AI backend can assign individual ID numbers per game/connection, and this helps to isolate connections.

It was fairly simple to set up, but I did run into many errors. For example, both the Python and Node.js libraries need to be partially compiled because they have external C dependencies.
When installing them, it attempts the compilation but it reported numerous errors without actually notifying me that I did not have a compiler installed.
Once I managed to install the dependencies, I ran into random errors of odd socket disconnects. I couldn't really figure out why, because the entire socket server ran on a thread - that means I could not actually output anything to the console.

To debug, I ended up opening files and writing to them, which was possible in the thread. This helped me figure out how to connect the sockets and fix any of the connectivity issues. Even now, the server has trouble connecting at times, but usually it works fine.

In the future, I think I would much rather write the entire application in a single language, because it would allow for much simpler integration.
