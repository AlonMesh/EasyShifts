import { useEffect, useState } from "react";

let socket_obj = null;

export function useSocket() {
    const [socket, setSocket] = useState(/** @type {WebSocket | null} */ (socket_obj));

    useEffect(() => {
        if (socket_obj == null) {
            // Establish WebSocket connection when the component mounts
            const newSocket = new WebSocket('ws://localhost:8080');

            // Event listener for WebSocket errors
            newSocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            // Event listener for WebSocket open
            newSocket.onopen = () => {
                console.log('WebSocket connection established successfully.');
            };

            // Update the socket state
            socket_obj = newSocket;
            setSocket(newSocket);
        }

        // No cleanup function here

    }, []);

    return socket;
}
