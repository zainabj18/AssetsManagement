import { VStack } from '@chakra-ui/react';
import { HStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, Input, Button } from '@chakra-ui/react';
import { Checkbox } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchTypesList } from '../api';
import { fetchTags } from '../api';
import { fetchProjects } from '../api';
import { fetchAssetClassifications} from '../api';

const AssetSearcher = ({filerFunc}) => {
	const [types, setTypes] = useState([]);
	const [classifications, setClassifications] = useState([]);
	const [projects, setProjects] = useState([]);
	const [tags, setTags] = useState([]);
	const [inputFields, setInputFields] = useState([
		{ name: '', values: '' }
	]);
	const [searchData, setSearchData] = useState(
		{ tags:[],types:[],projects:[],classifications:[],attributes:[]}
	);
	const handleCheckBoxChange = (name,id,value) => {
		console.log(name,id,value);
		let oldValues=searchData[name];
		console.log(oldValues);
		if (value){
			oldValues.push(id);
		}else{
			let index = oldValues.indexOf(id);
			if (index !== -1) {
				oldValues.splice(index, 1);
			}
		}

		setSearchData((prevAssetState) => ({
			...prevAssetState,
			[name]: oldValues,
		}));
		console.log(searchData);
	};

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

	const test = () => {
		filerFunc(searchData);
	};

	useEffect(() => {
		console.log(filerFunc);
		fetchTypesList().then((res) => {
			setTypes(res.data);
		}
		);

		fetchTags().then((res) => {
			setTags(res.data);

		}
		);

		fetchProjects().then((res) => {
			setProjects(res.data);
		}
		);

		fetchAssetClassifications().then((res) => {
			setClassifications(res.data);
			setSearchData((prevAssetState) => ({
				...prevAssetState,
				classifications: res.data,
			}));
		}

		
		);
	}, []);

	return (
		<Box p={30}>
			<Accordion defaultIndex={[0]} allowMultiple>
				<AccordionItem>

					<AccordionButton>Asset Type
						<AccordionIcon />
					</AccordionButton>

					<AccordionPanel pb={4}>
						<VStack align={'left'}>
							{types.map((type) => {
								return ( 
									<Checkbox  onChange={(e) => handleCheckBoxChange('types',type.type_id,e.target.checked)}>{type.type_name}</Checkbox>
								);
							})}
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
	
					<AccordionButton>
							Tags
						<AccordionIcon />
					</AccordionButton>
	
					<AccordionPanel pb={4}>
						<VStack align={'left'}>
							{tags.map((tag) => {
								return ( 
									<Checkbox  onChange={(e) => handleCheckBoxChange('tags',tag.id,e.target.checked)}>{tag.name}</Checkbox>
								);
							})}
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
				
					<AccordionButton>
							Projects
						<AccordionIcon />
					</AccordionButton>

					<AccordionPanel pb={4}>
						<VStack align={'left'}>
							{projects.map((project) => {
								return ( 
									<Checkbox  onChange={(e) => handleCheckBoxChange('projects',project.id,e.target.checked)}>{project.name}</Checkbox>
								);
							})}
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
	
					<AccordionButton>
							Access Levels
						<AccordionIcon />
					</AccordionButton>

					<AccordionPanel pb={4}>
						<VStack align={'left'}>
							{classifications.map((classification) => {
								return ( 
							
									<Checkbox  onChange={(e) => handleCheckBoxChange('classifications',classification,e.target.checked)}>{classification}</Checkbox>
								); 
							})}
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
									color='white'
								/>
								<Input
									name='values'
									placeholder='Attribute value'
									value={input.values}
									onChange={event => handleFormChange(index, event)}
									color='white'
									fontsize='20'
								/>
								<Button onClick={() => removeFields(index)}>Remove</Button>
							</HStack>
						);
					})}
					<Button onClick={addFields}>Add More</Button>
					<Button onClick={submit}>Submit</Button>
				</form>
			</div>
			<Button onClick={test}>Filter</Button>
		</Box>
	);
};
export default AssetSearcher;
