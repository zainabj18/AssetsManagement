
import { DeleteIcon } from '@chakra-ui/icons';
import {
	Box, Button, Center, FormControl,
	FormLabel,
	HStack, Heading, IconButton, Input, Stack
} from '@chakra-ui/react';
import React, { useState } from 'react';



const TypeAdder = () => {
	const [inputFields, setInputFields] = useState([
		{ attrName: 'Programming Language', attrType: 'text' },
		{ attrName: 'country of origin', attrType: 'text' }
	]);

	const addAttribute = () => {
		let newAttribute = { attrName: '', attrType: '' };
		setInputFields([...inputFields, newAttribute]);
	};

	const handleFormChange = (index, event) => {
		let data = [...inputFields];
		data[index][event.target.name] = event.target.value;
		setInputFields(data);
	};

	const deleteAttribute = (index) => {
		let data = [...inputFields];
		data.splice(index,1);
		setInputFields(data);
	};

	return (
		<Center height={'100vh'}>
			<Box bg={'white'} color={'black'} p={10} borderRadius={10} w={'1000px'} mx={'auto'} mb={'100px'}>
				<Heading mb={'25px'}>TypeAdder</Heading>
				<HStack spacing={'25px'}>
					<FormControl>
						<FormLabel>Name</FormLabel>
						<Input type='text' placeholder="Name" />
					</FormControl>
				</HStack>

				{inputFields.map((attr,index) => {return (
					<HStack key={index} alignItems={'end'} mt={8}>
						<FormControl>
							<FormLabel>Attribute Name</FormLabel>
							<Input type={'text'} placeholder={'Attribute name'} defaultValue={attr.attrName} onChange={event => handleFormChange(index, event)} name='attrName'/>
						</FormControl>
						<FormControl>
							<FormLabel>Data Type</FormLabel>
							<Input type={'text'} placeholder='Data type' defaultValue={attr.attrType} onChange={event => handleFormChange(index, event)} name='attrType'/>
						</FormControl>
						<IconButton
							icon={<DeleteIcon />}
							colorScheme='blue'
							onClick={event => deleteAttribute(index)}
						/>
					</HStack>);})}

				<Stack direction='row' align='center' mt={8}>
					<Button colorScheme='blue' variant='solid' size='md'>
            Save
					</Button>
					<Button colorScheme='red' variant='solid' size='md' onClick={addAttribute}>
            Add
					</Button>
				</Stack>
			</Box>
		</Center>
	);
};

export default TypeAdder;
