import React, { createContext, useState, useCallback, useContext } from 'react';
import axios from 'axios';
import { UserContext } from './UserContext';

export const DataContext = createContext();

export const DataProvider = ({ children }) => {
    const [selectedSite, setSelectedSite] = useState(null);
    const [previews, setPreviews] = useState([]);
    const { user } = useContext(UserContext);
    const [data, setData] = useState({
        color_palette: [],
        contrast_ratio: 0,
        harmony_score: 0,
        best_trait: '',
        analysis: '', // Add analysis to the data state
    });

    const fetchData = useCallback(async (url) => {
        if (!url) {
            console.error('URL is required for fetching data');
            return;
        }
        try {
            const response = await axios.post('http://localhost:5000/api/scrape', { url });
            console.log("API Response:", response.data);
            if (response.status === 200 && response.data) {
                const { color_palette, contrast_ratio, harmony_score, best_trait, analysis } = response.data; // Destructure analysis from response
                setData(prevData => ({
                    ...prevData,
                    color_palette: color_palette || [],
                    contrast_ratio: contrast_ratio || 0,
                    harmony_score: harmony_score || 0,
                    best_trait: best_trait || 'No dominant trait',
                    analysis: analysis || 'No analysis available', // Update analysis
                }));
            } else {
                console.error('Failed to fetch data:', response.data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error fetching data:', error.response ? error.response.data : error.message);
        }
    }, []);

    const selectSite = useCallback(async (siteId) => {
        if (!siteId) {
            console.error('Site ID is required for fetching full data');
            return;
        }
        try {
            const response = await axios.get(`http://localhost:5000/api/site-details/${siteId}`, {
                headers: { 'Authorization': `Bearer ${user.token}` }
            });
            if (response.data) {
                setData({
                    color_palette: response.data.color_palette || [],
                    contrast_ratio: response.data.contrast_ratio || 0,
                    harmony_score: response.data.harmony_score || 0,
                    best_trait: response.data.best_trait || 'No dominant trait',
                    analysis: response.data.analysis || 'No analysis available', // Update analysis
                });
                setSelectedSite(response.data);
            }
        } catch (error) {
            console.error('Error fetching full site data:', error.response ? error.response.data : error.message);
        }
    }, [user]);

    const saveData = useCallback(async () => {
        if (!user) {
            console.error('User not authenticated');
            return;
        }
        try {
            const response = await axios.post('http://localhost:5000/api/save', {
                url: data.url,
                color_palette: data.color_palette,
                contrast_ratio: data.contrast_ratio,
                harmony_score: data.harmony_score,
                best_trait: data.best_trait,
                analysis: data.analysis, // Include analysis in save request
            }, {
                headers: { 'Authorization': `Bearer ${user.token}` }
            });

            if (response.status === 201) {
                fetchPreviews();
            }
        } catch (error) {
            console.error('Error saving data:', error.response ? error.response.data : error.message);
        }
    }, [data, user, setPreviews]);

    const deleteData = useCallback(async (dataId) => {
        if (!user) {
            console.error('User not authenticated');
            return;
        }
        try {
            const response = await axios.delete(`http://localhost:5000/api/delete/${dataId}`, {
                headers: { 'Authorization': `Bearer ${user.token}` }
            });

            if (response.status === 200) {
                fetchPreviews();
            }
        } catch (error) {
            console.error('Error deleting data:', error.response ? error.response.data : error.message);
        }
    }, [user]);

    const fetchPreviews = useCallback(() => {
        if (!user) {
            console.error('User not authenticated');
            return;
        }
        axios.get(`http://localhost:5000/api/saved-sites-preview`, {
            headers: { Authorization: `Bearer ${user.token}` }
        })
        .then(response => {
            setPreviews(response.data);
        })
        .catch(error => console.error('Failed to fetch site previews', error));
    }, [user]);

    return (
        <DataContext.Provider value={{ data, fetchData, saveData, deleteData, fetchPreviews, previews, selectedSite, selectSite }}>
            {children}
        </DataContext.Provider>
    );
};


