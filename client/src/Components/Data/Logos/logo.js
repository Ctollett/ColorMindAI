import React, { useContext, useEffect } from 'react';
import { Typography, Paper, Box } from '@mui/material'; // Using Material-UI components for styling
import { DataContext } from '../../../Context/DataContext';

const DisplayLogo = ({ url }) => {
    const { data, fetchData } = useContext(DataContext);

    useEffect(() => {
        if (url) {
            fetchData(url);
        }
    }, [url, fetchData]); // Dependency array ensures fetchData is called only when url or fetchData changes

    return (
        <Box sx={{ padding: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography variant="h5" gutterBottom>Website Details</Typography>
            {data.website_name && <Typography variant="h6">{data.website_name}</Typography>}
            {data.logo_url && (
                <Paper elevation={3} sx={{ padding: 2, marginTop: 2 }}>
                    <img src={data.logo_url} alt="Website Logo" style={{ maxWidth: '100%', height: 'auto' }} />
                </Paper>
            )}
        </Box>
    );
};

export default DisplayLogo;

