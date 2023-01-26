import { Outlet } from 'react-router-dom';
import { Heading, VStack,Text } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';

const Layout = () => {
	const [api, setAPI] = useState();
	useEffect(() => {
		fetch('http://127.0.0.1:5000/api/v1/cr',{
			methods: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': 'true'
			}}).then((res) =>
			res.json().then((data) => {
				setAPI(data.version);
				console.log('hello');
			})
		);
	}, []);
	return (
		<VStack minW="100vw">
			<Heading>Code Groover Assets Metadata Repository</Heading>
			<Text>Using API version:{api}</Text>
			<Outlet />
		</VStack>
	);
};

export default Layout;
