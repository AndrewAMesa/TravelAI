import React, { useState } from 'react';
import ActionButton from './ActionButton';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import itineraryIcon from '../Images/itinerary.png';
import flightIcon from '../Images/plane.png';
import lodgingIcon from '../Images/hotel.png';

const Home = () => {
    const [messages, setMessages] = useState([]); // For messages
    const [input, setInput] = useState(''); // For user input
    const [loggedUser, setLoggedUser] = useState('YourUsername');
    const [chatHistory, setChatHistory] = useState([]);

    // Function to handle sending user input
    const handleSendMessage = async () => {
        if (input.trim() !== '') {
            // Add user input to messages
            const userMessage = { type: 'user', content: input };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            // Update chat history
            const newChatHistory = { title: input, date: new Date().toLocaleString() };
            setChatHistory((prevHistory) => [...prevHistory, newChatHistory]);

            setInput(''); // Clear the input field

            // Call the Flask API
            try {
                const response = await fetch('http://127.0.0.1:5000/run_trip_planner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ loggedUser, description: input }),
                });

                const data = await response.json();
                if (response.ok) {
                    // Add AI response to messages
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.plan },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.error },
                    ]);
                }
            } catch (error) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: 'ai', content: 'Error communicating with the server.' },
                ]);
            }
        }
    };

    // Function to handle "Find Flights" button click
    const handleFindFlights = async () => {
         if (input.trim() !== '') {
            // Add user input to messages
            const userMessage = { type: 'user', content: input };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            // Update chat history
            const newChatHistory = { title: input, date: new Date().toLocaleString() };
            setChatHistory((prevHistory) => [...prevHistory, newChatHistory]);

            setInput(''); // Clear the input field

            // Call the Flask API
            try {
                const response = await fetch('http://127.0.0.1:5000/run_flight_planner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ loggedUser, description: input }),
                });

                const data = await response.json();
                if (response.ok) {
                    // Add AI response to messages
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.plan },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.error },
                    ]);
                }
            } catch (error) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: 'ai', content: 'Error communicating with the server.' },
                ]);
            }
        }
    };

    // Function to handle "Find Flights" button click
    const handleFindLodging = async () => {
         if (input.trim() !== '') {
            // Add user input to messages
            const userMessage = { type: 'user', content: input };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            // Update chat history
            const newChatHistory = { title: input, date: new Date().toLocaleString() };
            setChatHistory((prevHistory) => [...prevHistory, newChatHistory]);

            setInput(''); // Clear the input field

            // Call the Flask API
            try {
                const response = await fetch('http://127.0.0.1:5000/run_lodging_planner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ loggedUser, description: input }),
                });

                const data = await response.json();
                if (response.ok) {
                    // Add AI response to messages
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.plan },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.error },
                    ]);
                }
            } catch (error) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: 'ai', content: 'Error communicating with the server.' },
                ]);
            }
        }
    };

    // Function to handle "Find Flights" button click
    const handleItineraryPlanning = async () => {
         if (input.trim() !== '') {
            // Add user input to messages
            const userMessage = { type: 'user', content: input };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            // Update chat history
            const newChatHistory = { title: input, date: new Date().toLocaleString() };
            setChatHistory((prevHistory) => [...prevHistory, newChatHistory]);

            setInput(''); // Clear the input field

            // Call the Flask API
            try {
                const response = await fetch('http://127.0.0.1:5000/run_itinerary_planner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ loggedUser, description: input }),
                });

                const data = await response.json();
                if (response.ok) {
                    // Add AI response to messages
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.plan },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: 'ai', content: data.error },
                    ]);
                }
            } catch (error) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: 'ai', content: 'Error communicating with the server.' },
                ]);
            }
        }
    };

    // Function to handle when a chat history item is clicked
    const handleChatClick = (chat) => {
        setMessages((prevMessages) => [
            { type: 'user', content: chat.title }, // Simulate user message
        ]);

        // Simulate AI response for the clicked chat
        setTimeout(() => {
            setMessages((prevMessages) => [
                ...prevMessages,
                { type: 'ai', content: 'This is a simulated AI response for the clicked chat.' },
            ]);
        }, 1000);
    };

    return (
        <div className="h-screen flex flex-col">
            {/* Top Bar */}
            <TopBar />

            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar Section */}
                <div className="w-1/4 bg-[#563635] text-white p-5">
                    <Sidebar chatHistory={chatHistory} onChatClick={handleChatClick} />
                </div>

                {/* Main Content Section */}
                <div className="w-3/4 flex flex-col bg-[#fad4c0] h-full">
                    {/* Action Buttons Section */}
                    {messages.length === 0 && (
                        <div className="grid grid-cols-3 ml-32 mb-1 mt-24 font-josefin">
                            <ActionButton label={"Find \nFlights"} icon={flightIcon} onClick={handleFindFlights} />
                            <ActionButton label={"Find \nLodging"} icon={lodgingIcon} onClick={handleFindLodging} />
                            <ActionButton label={"Itinerary \nPlanning"} icon={itineraryIcon} onClick={handleItineraryPlanning} />
                        </div>
                    )}

                    {/* Chat Section */}
                    <div className="flex-1 flex flex-col overflow-y-auto p-4">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex mb-2 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`p-3 rounded-3xl max-w-md font-josefin break-words whitespace-pre-wrap ${
                                        message.type === 'user' ? 'bg-white text-[#563635]' : 'bg-[#563635] text-white'
                                    }`}
                                >
                                    {message.content}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Input Section */}
                    <div className="w-full flex items-center bg-[#fadbca] shadow-2xl shadow-black p-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Search for flights, lodging, or destinations..."
                            className="p-1 bg-[#fadbca] w-full font-josefin text-[#563635] placeholder:text-[#563635] placeholder:text-opacity-60 mr-5"
                        />
                        <button
                            onClick={handleSendMessage}
                            className="p-3 bg-[#563635] text-white font-josefin rounded-full"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
