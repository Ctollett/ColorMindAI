import React, { useContext, useState, useEffect } from 'react';
import { UserContext } from '../../Context/UserContext';
import { Dialog, DialogContent, DialogTitle, TextField, Button, Typography, DialogActions } from '@mui/material';

function AuthForm({ open, handleClose }) {
    const { user, login, register, error, clearError } = useContext(UserContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');  
    const [isLogin, setIsLogin] = useState(true); 

    useEffect(() => {
        clearError();
    }, [isLogin]); 

    const handleAuth = (event) => {
        event.preventDefault();
        clearError();
        if (isLogin) {
            login(email, password);
        } else {
            register(username, email, password);
        }
    };

    const toggleForm = () => {
        setIsLogin(!isLogin);
        clearError();
        setEmail('');
        setPassword('');
        setUsername('');  
    };

    useEffect(() => {
        if (!user) {
            setEmail('');
            setPassword('');
            setUsername('');  
        }
    }, [user]);

    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{isLogin ? 'Login' : 'Register'}</DialogTitle>
            <DialogContent>
                {!isLogin && (
                    <TextField
                        autoFocus
                        margin="dense"
                        id="username"
                        label="Username"
                        type="text"
                        fullWidth
                        variant="outlined"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />
                )}
                <TextField
                    autoFocus={isLogin}
                    margin="dense"
                    id="email"
                    label="Email Address"
                    type="email"
                    fullWidth
                    variant="outlined"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                />
                <TextField
                    margin="dense"
                    id="password"
                    label="Password"
                    type="password"
                    fullWidth
                    variant="outlined"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                {error && (
                    <Typography color="error" variant="body2" style={{ marginTop: 8 }}>
                        {error}
                    </Typography>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} color="primary">
                    Cancel
                </Button>
                <Button onClick={handleAuth} color="primary">
                    {isLogin ? 'Login' : 'Register'}
                </Button>
                <Button onClick={toggleForm} color="primary">
                    {isLogin ? 'Need to register?' : 'Already have an account?'}
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AuthForm;





