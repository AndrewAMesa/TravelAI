import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { Icon } from '@iconify/react';

import {createNewUser} from "../Routes";

const TopBar = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showNewUser, setShowNewUser] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const toggleLoginPopup = () => {
    setShowLogin(!showLogin);
  };

  const toggleNewUserPopup = () => {
    setShowNewUser(!showNewUser);
    setShowLogin(false);
  };

  const LoginModal = (
    <div
      className="fixed inset-0 z-[9999] flex items-center justify-center bg-black bg-opacity-50"
      style={{
        zIndex: 9999,
        position: 'fixed',
        top: 0,
        left: 0,
        isolation: 'isolate',
      }}
    >
      <div className="bg-white p-8 rounded shadow-lg w-96 relative z-[10000]">
        <h2 className="text-2xl mb-6 font-bold text-gray-800">Login</h2>
        <form>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
              placeholder="Enter your username"
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
              placeholder="Enter your password"
            />
          </div>
          <button
            type="submit"
            className="bg-[#4e2c20] text-white px-4 py-2 rounded w-full hover:bg-[#6a4532]"
          >
            Login
          </button>
        </form>
        <button
          onClick={toggleNewUserPopup}
          className="mt-4 text-blue-600 underline block text-center"
        >
          New User? Register Here
        </button>
        <button
          onClick={toggleLoginPopup}
          className="mt-4 text-red-600 underline block text-center"
        >
          Close
        </button>
      </div>
    </div>
  );

  return (
    <div className="w-full h-16 bg-[#563635] flex items-center justify-between px-4 text-white drop-shadow-md">
      <h1 className="text-xl font-bold">AI Travel Assistant</h1>
      <div className="flex items-center space-x-4">
        <Icon
          icon="iconamoon:profile-circle-fill"
          onClick={toggleLoginPopup}
          className="w-12 h-12 hover:text-[#4e2c20] transition duration-200 cursor-pointer"
        />
      </div>

      {showLogin && ReactDOM.createPortal(LoginModal, document.getElementById('root'))}
    </div>
  );
};

export default TopBar;
