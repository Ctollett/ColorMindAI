/// src/components/AnalysisResults.js
import React, { useContext } from 'react';
import { DataContext } from '../../Context/DataContext';

function AnalysisResults() {
    const { data } = useContext(DataContext);

    return (
        <div>
            <h2>Design Analysis</h2>
            <p>{data.analysis}</p>
        </div>
    );
}

export default AnalysisResults;





