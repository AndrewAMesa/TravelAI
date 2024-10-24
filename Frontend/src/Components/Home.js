import React, { useState } from 'react';
import ActionButton from './ActionButton';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import itineraryIcon from '../Images/itinerary.png';
import flightIcon from '../Images/plane.png';
import lodgingIcon from '../Images/hotel.png';

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loggedUser, setLoggedUser] = useState('YourUsername');
  const [chatHistory, setChatHistory] = useState([]);
  const [buttonsShrink, setButtonsShrink] = useState(false);

  const handleMessage = async (endpoint) => {
    if (input.trim() !== '') {
      const userMessage = { type: 'user', content: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      const newChatHistory = { title: input, date: new Date().toLocaleString() };
      setChatHistory((prevHistory) => [...prevHistory, newChatHistory]);

      setInput('');
      setButtonsShrink(true);

      try {
        const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ loggedUser, description: input }),
        });

        const data = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: 'ai', content: response.ok ? data.plan : data.error },
        ]);
      } catch (error) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: 'ai', content: 'Error communicating with the server.' },
        ]);
      }
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <TopBar />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar Section */}
        <div className="w-1/4 bg-[#563635] text-white p-5">
          <Sidebar chatHistory={chatHistory} onChatClick={(chat) => {
            setMessages([{ type: 'user', content: chat.title }]);
            setTimeout(() => {
              setMessages((prevMessages) => [
                ...prevMessages,
                { type: 'ai', content: 'This is a simulated AI response for the clicked chat.' },
              ]);
            }, 1000);
          }} />
        </div>

        {/* Main Content Section */}
        <div className="w-3/4 flex flex-col bg-[#fad4c0] h-full items-center justify-center">
          {/* Buttons Section */}
          <div
            className={`flex w-full justify-around items-center transition-all duration-300 transform ${
              buttonsShrink ? 'py-8' : 'py-16'
            }`}
          >
            <ActionButton
              label="Find Flights"
              icon={flightIcon}
              onClick={() => handleMessage('run_flight_planner')}
              isSmall={buttonsShrink}
            />
            <ActionButton
              label="Find Lodging"
              icon={lodgingIcon}
              onClick={() => handleMessage('run_lodging_planner')}
              isSmall={buttonsShrink}
            />
            <ActionButton
              label="Itinerary Planning"
              icon={itineraryIcon}
              onClick={() => handleMessage('run_itinerary_planner')}
              isSmall={buttonsShrink}
            />
          </div>

        {/* Chat Section */}
        <div className="flex-1 flex flex-col overflow-y-auto p-4 w-full">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex mb-2 ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`p-3 rounded-xl font-josefin break-words whitespace-pre-wrap ${
                  message.type === 'user'
                    ? 'bg-white text-[#563635]'
                    : 'bg-[#563635] text-white'
                }`}
                style={{
                  maxWidth: '70%', // Limits how wide the message box can get
                  alignSelf: message.type === 'user' ? 'flex-end' : 'flex-start',
                }}
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
              className="p-2 bg-[#fadbca] w-full font-josefin text-[#563635] placeholder:text-[#563635] placeholder:text-opacity-60 mr-4"
            />
            <button
              onClick={() => handleMessage('run_trip_planner')}
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
