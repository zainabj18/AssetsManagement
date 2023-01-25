import { Outlet } from 'react-router-dom';
import { Heading, VStack,Text } from '@chakra-ui/react';
import { Input } from '@chakra-ui/react'
import React, { useState, useEffect } from 'react';
import {
	FormControl,
	FormLabel,
	FormErrorMessage,
	FormHelperText,
  } from '@chakra-ui/react'


const TypeAdder = () => {
	return (
		<VStack minW="100vw">
			<Text>TypeAdder</Text>
			<FormControl>
  				<FormLabel>Name</FormLabel>
  				<Input type='text' placeholder = 'Name'/>
			</FormControl>
			<FormControl>
  				<FormLabel>Attribute Name</FormLabel>
  				<Input type='text' placeholder = 'AttributeName'/>
			</FormControl>
			<FormControl>
  				<FormLabel>Data Type</FormLabel>
  				<Input type='text' placeholder = 'DataType'/>
			</FormControl>
		</VStack>
	);
};

export default TypeAdder;
