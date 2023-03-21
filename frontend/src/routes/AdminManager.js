import { Outlet, useNavigate } from 'react-router-dom';
import { Heading, VStack,Text, HStack } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { Input, Stack } from '@chakra-ui/react';
import { Button, ButtonGroup} from '@chakra-ui/react';
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
		<VStack display={"flex"} width="80vw" justifyContent={"flex-start"} alignItems="flex-start" overflow={"hidden"}>
			<Box  width={'72vw'} alignSelf="center" bg="white" marginY={5}>
			<Heading fontWeight={"bold"}  textAlign="center" paddingY="5px">AdminManager</Heading>
			{inputField.map((search, index) => {return (
				<Stack spacing={3} color={'black'}>
					<Input bg='white' placeholder='search' alignSelf={'center'} width={"90%"}type='text' border={"1px solid"}  top={25} defaultValue={search.username} onChange={event => handleFormChange(index, event)} name="username"/>
				</Stack>
			);})}
			<Stack pt={35}>
				<div style={{height:'50vh',overflow:"scroll",width:"100%"}}>
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
											<AccordionPanel pb={4} borderTop={'1px solid black'} display="flex" >
												<Button bg='#80aaff' color='#000' marginRight={1} onClick={accountDetails}>View Account Details</Button>
												<Button bg='#80aaff' color='#000'  marginX={1} onClick={pass_func}>Change Password</Button>
												<Button bg='#80aaff' color='#000'  onClick={handleRelatedProjects}>View Related Projects</Button>
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
											<AccordionPanel pb={4} borderTop={'1px solid black'}>
												<Button bg='#80aaff' color='#000'  marginRight={1} onClick={accountDetails}>View Account Details</Button>
												<Button bg='#80aaff' color='#000'  marginRight={2} onClick={pass_func}>Change Password</Button>
												<Button bg='#80aaff' color='#000' onClick={handleRelatedProjects}>View Related Projects</Button>
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
											<AccordionPanel pb={4} borderTop={'1px solid black'}>
												<Button bg='#80aaff' color='#000'  marginRight={1} onClick={accountDetails}>View Account Details</Button>
												<Button bg='#80aaff' color='#000'  marginRight={2} onClick={pass_func}>Change Password</Button>
												<Button bg='#80aaff' color='#000' onClick={handleRelatedProjects}>View Related Projects</Button>
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
													<Box as="span" flex='1' textAlign='left' >
													Edit Details
													</Box>
													<AccordionIcon />
												</AccordionButton>
											</h2>
											<AccordionPanel pb={4} borderTop={'1px solid black'} >
												<Button bg='#80aaff' color='#000'  marginRight={1} onClick={accountDetails}>View Account Details</Button>
												<Button bg='#80aaff' color='#000'  marginRight={2} onClick={pass_func}>Change Password</Button>
												<Button bg='#80aaff' color='#000' onClick={handleRelatedProjects}>View Related Projects</Button>
											</AccordionPanel>
										</AccordionItem>
									</Accordion>
								</Td>
							</Tr>
						</Tbody>
					</Table>
				</div>
			</Stack>
			<div style={{display:"flex",justifyContent:"center",alignItems:"center"}}>
				<Link href='/user' color="white"  bg="#ed7966" alignItems={'center'}  width={'30vw'} textAlign="center" rounded="2xl" alignSelf={'center'} ><Button color="white" display='flex'  width={'100%'} textAlign={'center'}  size={'lg'}>New</Button></Link>
			</div>
			</Box>
		</VStack>
    
	);
};

export default AdminManager;
