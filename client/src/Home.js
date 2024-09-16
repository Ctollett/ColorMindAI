import React, { useState } from 'react';
import { Box } from '@mui/material';
import Toolbar from '../src/Components/Toolbar/Toolbar';
import Sidebar from './Components/Sidebar/Sidebar';
import DataDisplay from './Components/DataDisplay/DataDisplay';

const Home = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <Toolbar onMenuClick={toggleSidebar} />
            <Box sx={{ display: 'flex', flexGrow: 1 }}>
                <Sidebar open={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
                <DataDisplay />
            </Box>
        </Box>
    );
};

export default Home;


