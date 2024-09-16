import React, { useContext } from 'react';
import { DataContext } from '../../Context/DataContext';

function Technologies() {
    const { data } = useContext(DataContext);

    return (
        <div className="technologies">
            <h2>Technologies Used</h2>
            <ul>
                {data.technologies.map((tech, index) => (
                    <li key={index}>{tech}</li>
                ))}
            </ul>
        </div>
    );
}

export default Technologies;
