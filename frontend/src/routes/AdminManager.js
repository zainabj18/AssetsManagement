import { useNavigate } from 'react-router-dom';
import { VStack, Text, Input, Stack, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, Accordion, AccordionItem, 
	AccordionButton, AccordionPanel, AccordionIcon, Box, Link,}
	from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
import { getUsers} from '../api';

const AdminManager = () => {

	const { user } = useAuth();
	let navigate = useNavigate();

	useEffect(() => {
		if (user && user.userRole !== 'ADMIN') {
			navigate('../');
		}
		
		async function loadUsers() {
			let data = await getUsers(res => res.data);
			setUsers(data.data);
		}
		loadUsers();
	},[]);

	const [searchText, setSearchText] = useState('');
	const [inputField, setInputField] = useState([{ username: ''}]);
	const [pass] = useState([{ pass: '' }]);
	const [relatedprojects] = useState([{ relatedproj: '' }]);

	const [users, setUsers] = useState([]);

	const handleFormChange =  (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
		setSearchText(data[0].username);
	};

	const pass_func = (e) => {
		e.preventDefault();
		console.log(pass);
	};

	const handleRelatedProjects = (e) => {
		e.preventDefault();
		console.log(relatedprojects);
	};

	return (
		<VStack minW="100vw">
			<Text>AdminManager</Text>
			{inputField.map((search, index) => {
				return (
					<Stack spacing={3} key = {index}>
						<Input  placeholder='search' size='lg' type='text' width={800} top={25} onChange={event => handleFormChange(index, event)} name="username" />
					</Stack>
				);
			})}
			<Stack pt={35}>
				<TableContainer>
					<Table variant='simple' size={'lg'}>
						<Thead>
							<Tr>
								<Th>First Name</Th>
								<Th>Last Name</Th>
								<Th>Username</Th>
								<Th>Account Type</Th>
								<Th>Account Privileges</Th>
								<Th></Th>
							</Tr>
						</Thead>
						<Tbody>
							{users.filter(user => user.username.toLowerCase().includes(searchText.toLowerCase())).map((user) => {
								return (
									<Tr key={user.accountID}>
										<Td>{user.firstName}</Td>
										<Td>{user.lastName}</Td>
										<Td>{user.username}</Td>
										<Td>{user.userRole}</Td>
										<Td>{user.userPrivileges}</Td>
										<Td>
											<Accordion allowToggle>
												<AccordionItem>
													<h2>
														<AccordionButton>
															<Box as="span" flex='1' textAlign='left'>
																Edit Details
															</Box>
															<AccordionIcon />
														</AccordionButton>
													</h2>
													<AccordionPanel pb={4}>
														<Button onClick={pass_func} variant='ghost'>Change Password</Button>
														<Button onClick={handleRelatedProjects} variant='ghost'>View Related Projects</Button>
													</AccordionPanel>
												</AccordionItem>
											</Accordion>
										</Td>
									</Tr>
								);
							})}
						</Tbody>
					</Table>
				</TableContainer>
			</Stack>
			<Stack>
				<Link href='/user'><Button right={370} colorScheme={'blue'} size={'lg'}>New</Button></Link>
			</Stack>
		</VStack>

	);
};

export default AdminManager;


