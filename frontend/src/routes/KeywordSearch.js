import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Data from './Data.js';
import { Card, Input } from 'semantic-ui-react';
import { filter } from '@chakra-ui/react';

export default function KeywordSearch() {
    const[APIData, setAPIData] = useState([]);
    const [filteredResults, setFilteredResults] = useState([]);
    //creating a state for the search input
    const [searchInput, setSearchInput] = useState('');
    useEffect(() => {
        //get request to fetch data 
        axios.get('src/routes/Data.js')
        .then((response) => {
            setAPIData(response.data);
        });
    }, []);

    //function to handle the search functionality
    const searchItems = (searchValue) => {
        setSearchInput(searchValue)
        if (searchInput !== '') {
            //filtering data through a method
            const filteredData = APIData.filter((item) => {
                //setting filtered array into a variable
                return Object.values(item.join('').toLowerCase().includes(searchInput.toLowerCase()))
            })
            setFilteredResults(filteredData)    
    } 
    else{
        setFilteredResults(APIData)
        }
    }


    //creating a search bar on he webpage
    return (
        <div style={{ padding: 20}}>
            <Input icon='search'
                placeholder='Search'
                //binding the search function to the search bar
                //whenever something is typed in, it will run the searchItems function
                onChange={(e) => searchItems(e.target.value)}
            />
        </div>
    );
}
