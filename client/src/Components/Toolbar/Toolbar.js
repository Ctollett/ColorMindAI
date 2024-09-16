import React from 'react';
import { AppBar, Toolbar as MuiToolbar, IconButton, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import InputForm from '../Input'; // Adjust the path as necessary

const Toolbar = ({ onMenuClick }) => {
    return (
        <AppBar position="static" sx={{
            backgroundColor: 'white',  // Set background color to white
            boxShadow: 'none',  // Remove drop shadow
            color: 'black',  // Set text color to black
            overflow: 'hidden'  // Prevents overflow issues with the form
        }}>
            <MuiToolbar>
                <Typography variant="h6" sx={{ flexGrow: 0, color: 'black', mr: 2 }}>
                    Your App
                </Typography>
                <InputForm />
                <IconButton edge="end" color="inherit" aria-label="menu" onClick={onMenuClick} sx={{ ml: 'auto' }}>
                    <MenuIcon />
                </IconButton>
            </MuiToolbar>
        </AppBar>
    );
};

export default Toolbar;

