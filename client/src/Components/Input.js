// src/Components/Input.j
import axios from 'axios';
// src/components/InputForm.js
import React, { useState, useContext } from 'react';
import { DataContext } from '../Context/DataContext';

function InputForm() {
    const [url, setUrl] = useState('');
    const { fetchData } = useContext(DataContext);

    const handleSubmit = async (event) => {
        event.preventDefault();
        fetchData(url);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Enter URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
            />
            <button type="submit">Submit</button>
        </form>
    );
}

export default InputForm;



