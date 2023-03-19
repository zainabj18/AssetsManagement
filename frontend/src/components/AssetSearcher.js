import { Container, Radio, RadioGroup, Select, Stack, VStack } from '@chakra-ui/react';
import { HStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, Input, Button } from '@chakra-ui/react';
import { Checkbox } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchTypesList } from '../api';
import { fetchAllAttributes,fetchTags } from '../api';
import { fetchProjects } from '../api';
import { fetchAssetClassifications} from '../api';

const RadioButtons=({name,changeFunc})=>{
	return (<RadioGroup defaultValue="OR" onChange={e=>changeFunc(name,e)}>
		<Stack spacing={5} direction='row'>
			<Radio value="OR" defaultChecked>OR</Radio>
			<Radio value="AND">AND</Radio>
		</Stack>
	</RadioGroup>);
};

const AssetSearcher = ({filerFunc}) => {
	const [types, setTypes] = useState([]);
	const [classifications, setClassifications] = useState([]);
	const [projects, setProjects] = useState([]);
	const [tags, setTags] = useState([]);
	const [attributes, setAttributes] = useState([]);
	const [tag, setTag] = useState(null);
	const [inputFields, setInputFields] = useState([
		{ attributeID: -1, attributeValue: 'name' }
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
	const handleToggle = (name,value) => {
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			[name]: value,
		}));
		console.log(searchData);
	};

	const handleFormChange = (index, event) => {
		let data = [...inputFields];
		data[index][event.target.name] = event.target.value;
		setInputFields(data);
	};

	const addFields = () => {
		let newfield = { attributeID: -1, attributeValue: 'name' };
		setInputFields([...inputFields, newfield]);
		console.log(inputFields);
	};

	const removeFields = (index) => {
		let data = [...inputFields];
		data.splice(index, 1);
		setInputFields(data);
	};

	const filter = () => {
		console.log(inputFields);
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			attributes: inputFields,
		}));


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
		}

		);

		fetchAllAttributes().then((res) => {
			let intial=[
				{attributeID: -1, attributeName: 'name', attributeType: 'text', validation: null},
				{attributeID: -2, attributeName: 'link', attributeType: 'text', validation: null},
				{attributeID: -3, attributeName: 'description', attributeType: 'text', validation: null}];
			setAttributes([...intial,...res]);
			
		});
	}, []);

	return (
		<Container>
			<Accordion defaultIndex={[0]} allowMultiple>
				<RadioButtons name="operation" changeFunc={handleToggle}/>
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
								<RadioButtons name="tagOperation" changeFunc={handleToggle}/>
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
								<RadioButtons name="projectOperation" changeFunc={handleToggle}/>
								<VStack align={'left'}>
									
									{projects.map((project) => {
										return ( 
											<Checkbox  onChange={(e) => handleCheckBoxChange('projects',project.id,e.target.checked)}>{project.name}</Checkbox>
										);
									})}
								</VStack>
							</AccordionPanel>
						</AccordionItem>	
					</AccordionPanel>
				</AccordionItem>
			</Accordion>
			<RadioButtons name="attributeOperation" changeFunc={handleToggle}/>
			

	
			{inputFields.map((input, index) => {
				return (
					<HStack key={index}>
						<Select  name='attributeID' value={input.attributeID} onChange={event => handleFormChange(index, event)}>
							{attributes.map((attribute, index) => {
								
				
								return <option value={attribute.attributeID}>{attribute.attributeName}</option>;})}
								
						</Select>
						<Select  name='operation' value={input.operation} onChange={event => handleFormChange(index, event)}>
								 <option value='EQUALS'>=</option>
								 <option value='LIKE'>LIKE</option>
								 <option value='HAS'>HAS</option>
						</Select>
						{input.operation !=='HAS' && 
						<Input
							name='attributeValue'
							placeholder='Attribute value'
							value={input.attributeValue}
							onChange={event => handleFormChange(index, event)}
							color='white'
							fontsize='20'
						/>}
						<Button onClick={() => removeFields(index)}>Remove</Button>
					</HStack>
				);
			})}
			<Button onClick={addFields}>Add More</Button>
			<Button onClick={filter}>Filter</Button>
		</Container>
	);
};
export default AssetSearcher;
