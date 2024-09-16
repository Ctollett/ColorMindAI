import React, { useContext, useEffect } from 'react';
import { Typography, Grid, Paper } from '@mui/material';
import { DataContext } from '../../../Context/DataContext';

function FontsDisplay() {
    const { data } = useContext(DataContext);

    useEffect(() => {
        console.log("Fonts data:", data.heading_fonts, data.subheading_fonts, data.paragraph_fonts);
    }, [data]);

    const renderFonts = (fonts) => (
        <Grid container spacing={1}>
            {fonts.map((font, index) => (
                <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
                    <Paper 
                        elevation={1} 
                        style={{ 
                            padding: '8px', 
                            textAlign: 'center', 
                            fontFamily: font, 
                            fontSize: '10px', 
                            height: '80px', 
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            overflow: 'hidden'
                        }}
                    >
                        {font}
                    </Paper>
                </Grid>
            ))}
        </Grid>
    );

    return (
        <div className="fonts-display" style={{ padding: '16px' }}>
            <Typography variant="h6" gutterBottom>Fonts Display</Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={4}>
                    <Typography variant="h6" gutterBottom>Heading Fonts</Typography>
                    {renderFonts(data.heading_fonts)}
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Typography variant="h6" gutterBottom>Subheading Fonts</Typography>
                    {renderFonts(data.subheading_fonts)}
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Typography variant="h6" gutterBottom>Paragraph Fonts</Typography>
                    {renderFonts(data.paragraph_fonts)}
                </Grid>
            </Grid>
        </div>
    );
}

export default FontsDisplay;
