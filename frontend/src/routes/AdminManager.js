import { Outlet, useNavigate } from 'react-router-dom';
import { Heading, VStack,Text, HStack } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { Input, Stack } from '@chakra-ui/react';
import { Button, ButtonGroup } from '@chakra-ui/react';
import {
	Table,
	Thead,
	Tbody,
	Tfoot,
	Tr,
	Th,
	Td,
	TableCaption,
	TableContainer,
} from '@chakra-ui/react';
import {
	Accordion,
	AccordionItem,
	AccordionButton,
	AccordionPanel,
	AccordionIcon,
	Box
} from '@chakra-ui/react';
import useAuth from '../hooks/useAuth';
import { Link } from '@chakra-ui/react';

const AdminManager = () => {

	const {user} = useAuth();
	let navigate=useNavigate();

	useEffect(() => {
		if (user && user.userRole!=='ADMIN'){
			navigate('../');
		}
	});	

	const [inputField, setInputField] = useState([{username: '' }]);
	const [accountdetails] = useState([{accdetails: ''}]);
	const [pass] = useState([{pass: ''}]);
	const [relatedprojects] =useState([{relatedproj: ''}]);

	const handleFormChange = (index, event) => {
		let data = [...inputField];
		data[index][event.target.name] = event.target.value;
		setInputField(data);
	};

	const newuser = (e) => {
		e.preventDefault();
		console.log(inputField);
	};

	const accountDetails = (e) => {
		e.preventDefault();
		console.log(accountdetails);
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
			{inputField.map((search, index) => {return (
				<Stack spacing={3} color={'black'}>
					<Input bg='white' placeholder='search' size='lg' type='text' width={800} top={25} defaultValue={search.username} onChange={event => handleFormChange(index, event)} name="username"/>
				</Stack>
			);})}
			<Stack pt={35}>
				<TableContainer>
					<Table size={'lg'}>
						<Thead>
							<Tr>
								<Th>First Name</Th>
								<Th>Last Name</Th>
								<Th>Username</Th>
								<Th></Th>
							</Tr>
						</Thead>
						<Tbody>
							<Tr>
								<Td>John</Td>
								<Td>Plat</Td>
								<Td>@John</Td>
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
												<Button bg='transparent' color='white' onClick={accountDetails}>View Account Details</Button>
												<Button bg='transparent' color='white' onClick={pass_func}>Change Password</Button>
												<Button bg='transparent' color='white' onClick={handleRelatedProjects}>View Related Projects</Button>
											</AccordionPanel>
										</AccordionItem>
									</Accordion>
								</Td>
							</Tr>
							<Tr>
								<Td>Ben</Td>
								<Td>Hatch</Td>
								<Td>@Ben</Td>
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
												<Button bg='transparent' color='white' onClick={accountDetails}>View Account Details</Button>
												<Button bg='transparent' color='white' onClick={pass_func}>Change Password</Button>
												<Button bg='transparent' color='white' onClick={handleRelatedProjects}>View Related Projects</Button>
											</AccordionPanel>
										</AccordionItem>
									</Accordion>
								</Td>
							</Tr>
							<Tr>
								<Td>Ben</Td>
								<Td>Smith</Td>
								<Td>@Ben.Smith</Td>
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
												<Button bg='transparent' color='white' onClick={accountDetails}>View Account Details</Button>
												<Button bg='transparent' color='white' onClick={pass_func}>Change Password</Button>
												<Button bg='transparent' color='white' onClick={handleRelatedProjects}>View Related Projects</Button>
											</AccordionPanel>
										</AccordionItem>
									</Accordion>
								</Td>
							</Tr>
							<Tr>
								<Td>Kate</Td>
								<Td>Barlow</Td>
								<Td>@Kate</Td>
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
												<Button bg='transparent' color='white' onClick={accountDetails}>View Account Details</Button>
												<Button bg='transparent' color='white' onClick={pass_func}>Change Password</Button>
												<Button bg='transparent' color='white' onClick={handleRelatedProjects}>View Related Projects</Button>
											</AccordionPanel>
										</AccordionItem>
									</Accordion>
								</Td>
							</Tr>
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
