import React, { useContext } from 'react';
import { Paper, Typography, Avatar, Grid, Button } from '@mui/material';
import { DataContext } from '../Context/DataContext';

const SitePreview = ({ site }) => {
    const { selectSite } = useContext(DataContext);

    return (
        <Grid item xs={12} sm={6} md={4} onClick={() => selectSite(site._id)}>
            <Paper elevation={0} sx={{ p: 2, textAlign: 'center', cursor: 'pointer' }}>
                <Avatar alt={site.website_name} src={site.logo_url || '/default-logo.png'} sx={{ width: 56, height: 56, mb: 1 }} />
                <Typography variant="body1">{site.website_name}</Typography>
            </Paper>
        </Grid>
    );
};

export default SitePreview;
