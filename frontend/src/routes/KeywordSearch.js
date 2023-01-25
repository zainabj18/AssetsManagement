import { useState } from 'react';
import Data from './Data.js';


export default function KeywordSearch() {
    const[query, setQuery] = useState('');


    return (
        <div className='KeywordSearch'>
            <label>Search</label>
            <input type='text' onChange={(e) => setQuery (e.target.value)} />
        </div>
    );
}
