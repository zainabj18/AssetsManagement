import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { filter, Input } from '@chakra-ui/react';
import AssetList from '../components/AssetList';

export default function KeywordSearch() {
	const [APIData, setAPIData] = useState([]);
	const [filteredResults, setFilteredResults] = useState([]);
	//creating a state for the search input
	const [searchInput, setSearchInput] = useState('');
	useEffect(() => {
		//get request to fetch data 
		axios.get('https://jsonplaceholder.typicode.com/users')
			.then((response) => {
				setAPIData(response.data);
			});
	}, []);

	//function to handle the search functionality
	const searchItems = (searchValue) => {
		setSearchInput(searchValue);
		if (searchInput !== '') {
			//filtering data through a method
			const filteredData = APIData.filter((item) => {
				//setting filtered array into a variable
				return Object.values(item.join('').toLowerCase().includes(searchInput.toLowerCase()));
			});
			setFilteredResults(filteredData);
		}
		else {
			setFilteredResults(APIData);
		}
	};


	//creating a search bar on he webpage
	return (
		<div style={{ padding: 20 }}>
			<AssetList />
		</div>
	);
}
