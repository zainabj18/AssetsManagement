import { Outlet } from 'react-router-dom';
import { Heading, VStack,Text } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { Input, Stack } from '@chakra-ui/react';

const AdminManager = () => {
	return (
		<VStack minW="100vw">
			<Text>AdminManager</Text>
			<Stack spacing={3} color={'black'}>
				<Input bg='white' placeholder='search' size='lg' type='text' width={800} top={100}/>
			</Stack>
		</VStack>
	);
};

export default AdminManager;
