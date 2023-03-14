import { useNavigate } from 'react-router-dom';
import { VStack, Text, Input, Stack, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, Accordion, AccordionItem, 
	AccordionButton, AccordionPanel, AccordionIcon, Box, Link} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
import { getUsers, getAccountDetails } from '../api';

const AdminManager = () => {

	const { user } = useAuth();
	let navigate = useNavigate();

	useEffect(() => {
		if (user && user.userRole !== 'ADMIN') {
			navigate('../');
		}
		async function loadUsers() {
			let data = await getUsers(res => res.data);
			console.log(data.data);
			setUsers(data.data);
		}
		loadUsers();
	},[]);

	const [inputField, setInputField] = useState([{ username: '' }]);
	const [accountdetails, setAccountDetails] = useState([{ accdetails: '' }]);
	const [pass] = useState([{ pass: '' }]);
	const [relatedprojects] = useState([{ relatedproj: '' }]);

	const [users, setUsers] = useState([]);
	const handleFormChange = (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
	};

	const loadAccountDetails = async (account_id) => {
		try {
			const res = await getAccountDetails(account_id);
			setAccountDetails(res.data);
			console.log(accountdetails);
			navigate('/user');
		} catch (e) {
			console.error(e);
		}
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
					<Stack spacing={3} color={'black'} key = {index}>
						<Input bg='white' placeholder='search' size='lg' type='text' width={800} top={25} defaultValue={search.username} onChange={event => handleFormChange(index, event)} name="username" />
					</Stack>
				);
			})}
			<Stack pt={35}>
				<TableContainer color='white'>
					<Table variant='simple' size={'lg'}>
						<Thead>
							<Tr>
								<Th color={'white'}>First Name</Th>
								<Th color={'white'}>Last Name</Th>
								<Th color={'white'}>Username</Th>
								<Th color={'white'}></Th>
							</Tr>
						</Thead>
						<Tbody>
							{users.map((user) => {
								return (
									<Tr key={user.accountID}>
										<Td>{user.firstName}</Td>
										<Td>{user.lastName}</Td>
										<Td>{user.username}</Td>
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
														<Button bg='transparent' color='white' onClick={() => loadAccountDetails(user.account_id)}>View Account Details</Button>
														<Link href='/login'> <Button bg='transparent' color='white' onClick={pass_func}>Change Password</Button></Link>
														<Link href='/projects/'><Button bg='transparent' color='white' onClick={handleRelatedProjects}>View Related Projects</Button></Link>
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
