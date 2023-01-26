import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Data from './Data.js';
import { Card, Input } from 'semantic-ui-react';
import { filter } from '@chakra-ui/react';

export default function KeywordSearch() {
    const[APIData, setAPIData] = useState([]);
    useEffect(() => {
        //get request to fetch data 
        axios.get('src/routes/Data.js')
        .then((response) => {
            setAPIData(response.data);
        });
    }, []);


    //creating a search bar on he webpage
    return (
        <div style={{ padding: 20}}>
            <Input icon='search'
                placeholder='Search'
            />
        </div>
    );
}
