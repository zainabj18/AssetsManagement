import { useNavigate } from 'react-router-dom';
import { VStack, Text, Input, Stack, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, Accordion, AccordionItem, 
	AccordionButton, AccordionPanel, AccordionIcon, Box, Link, Modal, ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton, useDisclosure,}
	from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
import { getUsers, getAccountDetails } from '../api';

const AdminManager = () => {

	const { user } = useAuth();
	let navigate = useNavigate();
	const { isOpen, onOpen, onClose } = useDisclosure();

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
	const [accountdetails, setAccountDetails] = useState([]);
	const [pass] = useState([{ pass: '' }]);
	const [relatedprojects] = useState([{ relatedproj: '' }]);

	const [users, setUsers] = useState([]);

	const handleFormChange =  (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
		setSearchText(data[0].username);
	};

	

	/*const loadAccountDetails = async (account_id) => {
		try {
			const res = await getAccountDetails(account_id);
			setAccountDetails(res.data);
			console.log(accountdetails);
		} catch (e) {
			console.error(e);
		}
	};*/

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
														<Button onClick={onOpen}>View Account Details</Button>
														<Modal isOpen={isOpen} onClose={onClose} size='xl' isCentered>
															<ModalOverlay />
															<ModalContent>
																<ModalHeader>Account Details</ModalHeader>
																<ModalCloseButton />
																<ModalBody></ModalBody>
																<ModalFooter>
																	<Button mr={3} onClick={onClose}>Close</Button>
																</ModalFooter>
															</ModalContent>
														</Modal>
														<Link href='/login'> <Button onClick={pass_func}>Change Password</Button></Link>
														<Link href='/projects/'><Button onClick={handleRelatedProjects}>View Related Projects</Button></Link>
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

