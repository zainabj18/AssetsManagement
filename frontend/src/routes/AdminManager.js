import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import { Box, Heading, VStack, Input, Stack, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, Link, Badge} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { getUsers, deleteUserAcc } from '../api';

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
	}, []);

	const [searchText, setSearchText] = useState('');
	const [inputField, setInputField] = useState([{ username: '' }]);
	const [users, setUsers] = useState([]);
	const [deleteuser, setDeleteUser] = useState([{ delete: '' }]);

	const handleFormChange = (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
		setSearchText(data[0].username);
	};

	const deleteUser = async (userIdToDelete) => {
		if (userIdToDelete === 1) {
			alert('Can not delete admin account.');
		}
		else {
			try {
				await deleteUserAcc(userIdToDelete);
				let data = [...deleteuser];
				const indexToDelete = data.findIndex(user => user.id === userIdToDelete);
				data.splice(indexToDelete, 1);
				setDeleteUser(data);
				window.location.reload();
			} catch (error) {
				console.error(error);
			}
		}
	};

	return (
		<VStack display={'flex'} width='60vw' justifyContent={'flex-start'} alignItems='flex-start' overflow={'hidden'} rounded='2xl'>
			<Box width={'100%'} alignSelf='center' bg='white' marginY={5} rounded='2xl' height={'80vh'}>
				<Heading fontWeight={'bold'} textAlign='center' paddingY='5px'>AdminManager</Heading>
				{inputField.map((search, index) => {
					return (
						<Stack spacing={3} color={'black'} key={index}>
							<Input bg='white' placeholder='Search Username' alignSelf={'center'} width={'90%'} type='text' border={'1px solid'} top={25} onChange={event => handleFormChange(index, event)} name='username' />
						</Stack>
					);
				})}
				<Stack pt={35}>
					<div style={{ height: '60vh', overflow: 'auto', width: '100%', borderRadius: 10 }}>
						<TableContainer>
							<Table variant='simple'>
								<Thead>
									<Tr>
										<Th>First Name</Th>
										<Th>Last Name</Th>
										<Th>Username</Th>
										<Th>Account Type</Th>
										<Th>Data Classification</Th>
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
												<Td><Badge bg={user.userRole}>{user.userRole}</Badge></Td>
												<Td><Badge bg={user.userRole}>{user.userPrivileges}</Badge></Td>
												<Td><Button variant='ghost' onClick={() => deleteUser(user.accountID)}>Delete User</Button></Td>
											</Tr>
										);
									})}
								</Tbody>
							</Table>
						</TableContainer>
					</div>
				</Stack>
				<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
					<Link href='./new' color='white' bg='#ed7966' alignItems={'center'} width={'30vw'} textAlign='center' rounded='2xl' alignSelf={'center'}>
						<Button color='white' display='flex' width={'100%'} textAlign={'center'} size={'lg'}>New</Button>
					</Link>
				</div>
			</Box>
		</VStack>
	);
};

export default AdminManager;
