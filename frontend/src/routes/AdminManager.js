import { Outlet } from 'react-router-dom';
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

const AdminManager = () => {
	return (
		<VStack minW="100vw">
			<Text>AdminManager</Text>
			<Stack spacing={3} color={'black'}>
				<Input bg='white' placeholder='search' size='lg' type='text' width={800} top={25}/>
			</Stack>
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
												<Button bg='transparent' color='white'>View Account Details</Button>
												<Button bg='transparent' color='white'>Change Password</Button>
												<Button bg='transparent' color='white'>View Related Projects</Button>
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
												<Button bg='transparent' color='white'>View Account Details</Button>
												<Button bg='transparent' color='white'>Change Password</Button>
												<Button bg='transparent' color='white'>View Related Projects</Button>
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
												<Button bg='transparent' color='white'>View Account Details</Button>
												<Button bg='transparent' color='white'>Change Password</Button>
												<Button bg='transparent' color='white'>View Related Projects</Button>
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
												<Button bg='transparent' color='white'>View Account Details</Button>
												<Button bg='transparent' color='white'>Change Password</Button>
												<Button bg='transparent' color='white'>View Related Projects</Button>
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
				<Button right={370} colorScheme='blue' size={'lg'}>New</Button>
			</Stack>	
		</VStack>
    
	);
};

export default AdminManager;
