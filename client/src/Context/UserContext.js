import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Retrieve token and user info from localStorage when the app loads
    useEffect(() => {
        const token = localStorage.getItem('token');
        const userInfo = localStorage.getItem('user');
        if (token && userInfo) {
            setUser({ ...JSON.parse(userInfo), token });
        }
    }, []);

    const authenticate = (token, user) => {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        setUser({ ...user, token });
        navigate('/');
    };

    const clearError = () => {
        setError(null);
    };

    const login = async (email, password) => {
        try {
            const response = await axios.post('http://localhost:5000/api/login', { email, password });
            if (response.data.message === 'Email not verified. Please check your email to verify your account.') {
                setError(response.data.message);
            } else {
                authenticate(response.data.token, response.data.user);
            }
        } catch (err) {
            if (err.response && err.response.status === 403) {
                setError('Email not verified. Please check your email to verify your account.');
            } else if (err.response && err.response.status === 401) {
                setError('Invalid email or password.');
            } else {
                setError('Login failed. Please check your credentials.');
            }
            console.error('Login error:', err);
        }
    };

    const register = async (username, email, password) => {
        try {
            const response = await axios.post('http://localhost:5000/api/register', { username, email, password });
            setError(response.data.message);  // Set the response message as an error to display it
        } catch (err) {
            if (err.response && err.response.status === 400) {
                setError(err.response.data.message);  // Display the specific error message from the server
            } else {
                setError('Registration failed. Please check your credentials.');
            }
            console.error('Registration error:', err);
        }
    };

    const logout = async () => {
        try {
            await axios.post('http://localhost:5000/api/logout', {}, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            setUser(null);
            navigate('/');
        } catch (err) {
            setError('Failed to logout.');
            console.error('Logout error:', err);
        }
    };

    return (
        <UserContext.Provider value={{ user, error, login, logout, register, clearError }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
