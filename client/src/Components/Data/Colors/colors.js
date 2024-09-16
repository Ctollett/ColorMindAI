import React, { useContext, useState } from 'react';
import { DataContext } from '../../../Context/DataContext';
import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import { useSnackbar } from 'notistack';

function ColorsDisplay() {
    const { data } = useContext(DataContext);
    const { enqueueSnackbar } = useSnackbar();
    const [copiedColor, setCopiedColor] = useState(null); // State to track the copied color

    const getMaxHeight = (index) => 100 - (index * 15);

    const handleColorClick = (color) => {
        navigator.clipboard.writeText(color).then(() => {
            enqueueSnackbar('Color copied to clipboard!', { variant: 'success' });
            setCopiedColor(color); // Set this color as copied
            setTimeout(() => setCopiedColor(null), 2000); // Reset after 2 seconds
        }).catch(err => {
            enqueueSnackbar('Failed to copy color!', { variant: 'error' });
            console.error('Failed to copy color:', err);
        });
    };

    return (
        <Box sx={{
            flexGrow: 1,
            padding: 2,
            maxWidth: '90vw', // Increase maximum width
            margin: 'auto' // Center the box if it's not taking up the full width of its parent
        }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Typography variant="h4" gutterBottom>
                        Color Analysis
                    </Typography>
                </Grid>
                <Grid item xs={12} md={5}>
                    <Box sx={{ 
                        height: '600px', // Combined height for both sections
                        width: '100%', // Set fixed width
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'space-between'
                    }}>
                        <Card variant="outlined" sx={{ 
                            boxShadow: 'none', 
                            border: 'none', 
                            height: '70%', // Height for the color palette section
                            width: '100%', // Set fixed width
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden' // Prevent overflow
                        }}>
                            <CardContent sx={{ overflowY: 'auto', }}>
                                <Typography variant="h6" color="textSecondary">
                                    Color Palette
                                </Typography>
                                <Box sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    
                                    height: 'calc(100% - 48px)', // Adjust height to fit within the CardContent
                                }}>
                                    {data.color_palette.map((color, index) => (
                                        <Box key={index} sx={{
                                            width: '100%',
                                            height: `${getMaxHeight(index)}px`,
                                            bgcolor: color,
                                            position: 'relative',
                                            overflow: 'hidden',
                                            cursor: 'pointer'
                                        }} onClick={() => handleColorClick(color)}>
                                            <Typography variant="body2" sx={{
                                                position: 'absolute',
                                                width: '100%',
                                                height: '100%',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                color: '#fff',
                                                transition: 'opacity 0.3s ease-in-out',
                                                '&:hover': {
                                                    backgroundColor: 'rgba(0,0,0,0.7)',
                                                    opacity: 1
                                                }
                                            }}>
                                                {copiedColor === color ? "Copied!" : color}
                                            </Typography>
                                        </Box>
                                    ))}
                                </Box>
                            </CardContent>
                        </Card>
                        <Card variant="outlined" sx={{ 
                            boxShadow: 'none', 
                            border: 'none', 
                            height: '30%', // Height for the detailed information section
                            width: '100%', // Set fixed width
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden' // Prevent overflow
                        }}>
                            <CardContent sx={{ overflowY: 'auto' }}>
                                <Typography variant="h6" color="textSecondary">
                                    Detailed Information
                                </Typography>
                                <Typography variant="body1">
                                    <strong>Best Color Trait:</strong> {data.best_trait}
                                </Typography>
                                <Typography variant="body1">
                                    <strong>Harmony Score:</strong> {data.harmony_score}
                                </Typography>
                                <Typography variant="body1">
                                    <strong>Contrast Ratio:</strong> {data.contrast_ratio}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Box>
                </Grid>
                <Grid item xs={12} md={7}>
                    <Card variant="outlined" sx={{ 
                        boxShadow: 'none', 
                        border: 'none', 
                        height: '600px', // Set fixed height for the analysis section
                        width: '100%', // Set fixed width
                        display: 'flex',
                        flexDirection: 'column',
                        overflow: 'hidden' // Prevent overflow
                    }}>
                        <CardContent>
                            <Typography variant="h6" color="textSecondary">
                                Analysis
                            </Typography>
                            <Typography variant="body1" sx={{ overflowY: 'auto', fontSize: '13px'}}>
                                {data.analysis} {/* Replace with your actual analysis data */}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}

export default ColorsDisplay;



