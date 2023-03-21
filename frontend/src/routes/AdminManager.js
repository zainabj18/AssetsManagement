import { useNavigate } from 'react-router-dom';
import { VStack, Text, Input, Stack, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, Link,}
	from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
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
	},[]);

	const [searchText, setSearchText] = useState('');
	const [inputField, setInputField] = useState([{ username: ''}]);
	const [relatedprojects] = useState([{ relatedproj: '' }]);
	const [users, setUsers] = useState([]);
	const [deleteuser, setDeleteUser] = useState([{delete: ''}]);

	const handleFormChange =  (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
		setSearchText(data[0].username);
	};

	const handleRelatedProjects = (e) => {
		e.preventDefault();
		console.log(relatedprojects);
	};

	const deleteUser = async (userIdToDelete) => {
		try {
			await deleteUserAcc(userIdToDelete);
			let data = [...deleteuser];
			const indexToDelete = data.findIndex(user => user.id === userIdToDelete);
			data.splice(indexToDelete, 1);
			setDeleteUser(data);
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<VStack minW="100vw">
			<Text>AdminManager</Text>
			{inputField.map((search, index) => {
				return (
					<Stack spacing={3} key = {index}>
						<Input placeholder='username search' size='lg' type='text' width={800} top={25} onChange={event => handleFormChange(index, event)} name="username" />
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
										<Td>{user.userRole}</Td>
										<Td>{user.userPrivileges}</Td>
										<Td><Button variant='ghost' onClick={() => deleteUser(user.accountID)}>Delete User</Button></Td>
										<Td><Button onClick={handleRelatedProjects} variant='ghost'>View Related Projects</Button></Td>	
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


