import React, { useState, useContext, useEffect } from 'react';
import { Box, Typography, Button, Dialog, Grid } from '@mui/material';
import { UserContext } from '../../Context/UserContext';
import { DataContext } from '../../Context/DataContext';
import AuthForm from '../Login/AuthForm';
import SitePreview from '../SitePreview'; // Ensure this component is capable of handling onClick events

const Sidebar = ({ open }) => {
    const [modalOpen, setModalOpen] = useState(false);
    const { user, logout } = useContext(UserContext);
    const { previews, fetchPreviews, deleteData, selectSite } = useContext(DataContext); // Ensure selectSite is provided by DataContext

    useEffect(() => {
        if (user && user.token) {
            fetchPreviews();
        }
    }, [user, fetchPreviews]);

    const handleOpenModal = () => setModalOpen(true);
    const handleCloseModal = () => setModalOpen(false);
    const handleLogout = () => logout();

    return (
        <>
            <Box sx={{
                width: 440, 
                flexShrink: 0, 
                transform: open ? 'translateX(0)' : 'translateX(100%)', 
                transition: 'transform 0.3s ease-in-out', 
                position: 'absolute', 
                top: 74, 
                right: 0, 
                height: 'calc(100% - 74px)', 
                bgcolor: 'background.paper', 
                overflow: 'auto', 
                zIndex: 1200
            }}>
                <Typography variant="h6" sx={{ p: 2 }}>
                    {user ? `Welcome, ${user.username}` : "Please log in to view saved sites"}
                </Typography>
                {user ? (
                    <>
                        <Typography sx={{ p: 2 }}>Here are your saved sites:</Typography>
                        <Grid container spacing={2}>
                            {previews?.length ? previews.map((site, index) => (
                                <SitePreview key={index} site={site} onDelete={deleteData} onSelect={selectSite} />
                            )) : <Typography sx={{ p: 2 }}>No sites saved yet.</Typography>}
                        </Grid>
                        <Button variant="contained" color="primary" onClick={handleLogout} sx={{ m: 2 }}>Logout</Button>
                    </>
                ) : (
                    <>
                        <Typography sx={{ p: 2 }}>Login to save and view results.</Typography>
                        <Button variant="contained" color="primary" onClick={handleOpenModal} sx={{ m: 2 }}>Login</Button>
                    </>
                )}
            </Box>
            <Dialog open={modalOpen} onClose={handleCloseModal}>
                <AuthForm open={modalOpen} handleClose={handleCloseModal} />
            </Dialog>
        </>
    );
};

export default Sidebar;






