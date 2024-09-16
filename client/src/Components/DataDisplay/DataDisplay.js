import React, { useContext } from 'react';
import axios from 'axios';
import { Button, Grid, Paper } from '@mui/material';
import { DataContext } from '../../Context/DataContext';
import { useUser } from '../../Context/UserContext';
import FontsDisplay from '../Data/Fonts/fonts';
import ColorsDisplay from '../Data/Colors/colors';

function DataDisplay() {
    const { data, saveData } = useContext(DataContext);
    const { user } = useUser(); // Get the user and token from UserContext

    const handleSave = () => {
        if (!user?.token) {
            alert('User is not authenticated');
            return;
        }
        saveData(); // Call the saveData function from context
    };

    return (
        <div className="data-display" style={{ padding: '16px' }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Paper elevation={0} style={{ height: '100%', minHeight: '300px', border: '1px solid #ddd', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', borderRadius: 60 }}>
                        <ColorsDisplay />
                    </Paper>
                </Grid>
                <Grid item xs={12} style={{ textAlign: 'center', marginTop: '16px' }}>
                    <Button onClick={handleSave} variant="contained" color="primary">
                        Save Data
                    </Button>
                </Grid>
            </Grid>
        </div>
    );
}

export default DataDisplay;
