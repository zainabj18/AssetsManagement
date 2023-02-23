import { VStack } from '@chakra-ui/react';
import { HStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import {Accordion,AccordionItem,AccordionButton,AccordionPanel,AccordionIcon, Input,Button} from '@chakra-ui/react';
import { Checkbox } from '@chakra-ui/react';
import { useState } from 'react';

const FilterBasedSearch = () => {
	const [inputFields, setInputFields] = useState([
		{ name: '', values: ''}
	]);

	const handleFormChange = (index, event) => {
		let data = [...inputFields];
		data[index][event.target.name] = event.target.value;
		setInputFields(data);
	};

	const addFields = () => {
		let newfield = { name: '', values: '' };
		setInputFields([...inputFields, newfield]);
	};

	const submit = (e) => {
		e.preventDefault();
		console.log(inputFields);
	};

	const removeFields = (index) => {
		let data = [...inputFields];
		data.splice(index, 1);
		setInputFields(data);
	};

	return (
		<Box p={30}>
			<VStack> <p>This is the Filter Based Search Page !!</p></VStack>
			<Accordion defaultIndex={[0]} allowMultiple>
				<AccordionItem>
					<h2>
						<AccordionButton>Asset Type
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Framework</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Documentation</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Tags
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>React</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Projects
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Project A</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project B</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project C</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project D</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Access Levels
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Public</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Internal</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Restricted</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Confidential</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
			</Accordion>
			<div className="App">
				<form onSubmit={submit}>
					{inputFields.map((input, index) => {
						return (
							<HStack key={index}>
								<Input
									name='name'
									placeholder='Attribute name'
									value={input.name}
									onChange={event => handleFormChange(index, event)}
									color = 'white'
								/>
								<Input
									name='values'
									placeholder='Attribute value'
									value={input.values}
									onChange={event => handleFormChange(index, event)}
									color = 'white'
									fontsize = '20'
								/>
								<Button onClick={() => removeFields(index)}>Remove</Button>
							</HStack>
						);
					})}
				</form>
    		</div>
			<VStack>
				<Button onClick={addFields}>Add More</Button>
				<Button onClick={submit}>Submit</Button>
			</VStack>
		</Box>
	);
};
export default FilterBasedSearch;
