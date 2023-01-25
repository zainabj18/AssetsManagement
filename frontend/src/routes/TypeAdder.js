import { Outlet } from 'react-router-dom';
import { Heading, VStack,Text } from '@chakra-ui/react';
import { Input } from '@chakra-ui/react'
import React, { useState, useEffect } from 'react';
import {
	FormControl,
	FormLabel,
	HStack,
	FormErrorMessage,
	FormHelperText,
  } from '@chakra-ui/react'
import { Button, ButtonGroup } from '@chakra-ui/react'



const TypeAdder = () => {
	const [inputFields, setInputFields] = useState([
		{ attrName: 'programming language', attrType: 'text' },
		{ attrName: 'country of origin', attrType: 'text' }
	  ])
	const addAttribute = () => {
		let newAttribute = { attrName: '', attrType: '' }
		setInputFields([...inputFields, newAttribute])
	}
	const handleFormChange = (index, event) => {
    	let data = [...inputFields];
    	data[index][event.target.name] = event.target.value;
		console.log(data)
		setInputFields(data)
	}
	return (
		<VStack minW="100vw">
			<Text>TypeAdder</Text>
			<FormControl isRequired>
  				<FormLabel>Name</FormLabel>
  				<Input type='text' placeholder = 'Name'/>
			</FormControl>
			{inputFields.map((attr,index) => {return (
				<HStack key={index}>
				<FormControl>
					<FormLabel>Attribute Name</FormLabel>
					<Input type='text' placeholder = 'AttributeName' defaultValue = {attr.attrName} onChange={event => handleFormChange(index, event)} name='attrName'/>
				</FormControl>
				<FormControl>
					<FormLabel>Data Type</FormLabel>
					<Input type='text' placeholder = 'DataType' defaultValue = {attr.attrType} onChange={event => handleFormChange(index, event)} name='attrType'/>
				</FormControl>
			</HStack>)})}
			
			<Button colorScheme='blue' onClick={addAttribute}>Add</Button>
			<Button colorScheme='blue'>Save</Button>
		</VStack>
	);
};

export default TypeAdder;
