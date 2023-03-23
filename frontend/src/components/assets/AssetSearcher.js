import { Radio, RadioGroup, Select, Stack, VStack } from '@chakra-ui/react';
import { HStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import { Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, Input, Button } from '@chakra-ui/react';
import { Checkbox } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { fetchAllAttributes, fetchTags, fetchTypesNamesVersionList } from '../../api';
import { fetchProjects } from '../../api';
import { fetchAssetClassifications } from '../../api';

const RadioButtons = ({ name, changeFunc }) => {
	return (<RadioGroup defaultValue='OR' onChange={e => changeFunc(name, e)} marginY={4}>
		<Stack spacing={5} direction='row'>
			<Radio value='OR' defaultChecked borderColor={'#0a2861 '}>OR</Radio>
			<Radio value='AND' borderColor={'#0a2861'}>AND</Radio>
		</Stack>
	</RadioGroup>);
};

const AssetSearcher = ({ filerFunc }) => {
	const [types, setTypes] = useState([]);
	const [classifications, setClassifications] = useState([]);
	const [projects, setProjects] = useState([]);
	const [tags, setTags] = useState([]);
	const [attributes, setAttributes] = useState([]);
	const [searchData, setSearchData] = useState(
		{ tags: [], types: [], projects: [], classifications: [], attributes: [] }
	);
	const handleCheckBoxChange = (name, id, value) => {
		console.log(name, id, value);
		let oldValues = searchData[name];
		console.log(oldValues);
		if (value) {
			oldValues.push(id);
		} else {
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
	const handleToggle = (name, value) => {
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			[name]: value,
		}));
		console.log(searchData);
	};

	const handleFormChange = (index, event) => {
		let data = searchData['attributes'];
		data[index][event.target.name] = event.target.value;
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			attributes: data,
		}));
	};

	const addFields = () => {
		let newfield = [...searchData['attributes'], { attributeID: -1, attributeValue: '' }];
		console.log('new fieedls');
		console.log(newfield);
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			attributes: newfield,
		}));
		console.log(searchData);
	};

	const removeFields = (index) => {
		let data = searchData['attributes'];
		data.splice(index, 1);
		setSearchData((prevAssetState) => ({
			...prevAssetState,
			attributes: data,
		}));
	};

	const filter = () => {
		console.log(searchData);
		filerFunc(searchData);
	};



	useEffect(() => {
		console.log(filerFunc);
		fetchTypesNamesVersionList().then((res) => {
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
			let intial = [
				{ attributeID: -1, attributeName: 'name', attributeType: 'text', validation: null },
				{ attributeID: -2, attributeName: 'link', attributeType: 'text', validation: null },
				{ attributeID: -3, attributeName: 'description', attributeType: 'text', validation: null }];
			setAttributes([...intial, ...res.data]);

		});
	}, []);

	return (
		<Box display={'flex'} flexDirection='column' width={'100%'} >
			<Accordion defaultIndex={[0]} allowMultiple>
				<RadioButtons name='operation' changeFunc={handleToggle} />
				<AccordionItem>

					<AccordionButton>Access Levels
						<AccordionIcon />
					</AccordionButton>

					<AccordionPanel pb={4}>
						<VStack align={'left'} overflowY='scroll' maxH='70vh' >
							{classifications.map((classification) => {
								return (

									<Checkbox onChange={(e) => handleCheckBoxChange('classifications', classification, e.target.checked)}>{classification}</Checkbox>
								);
							})}
						</VStack>
						<AccordionItem>

							<AccordionButton>Asset Type
								<AccordionIcon />
							</AccordionButton>

							<AccordionPanel pb={4} overflowY='scroll' maxH='70vh' >
								<VStack align={'left'}>
									{types.map((type) => {
										return (
											<Checkbox onChange={(e) => handleCheckBoxChange('types', type.version_id, e.target.checked)}>{type.type_name}</Checkbox>
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

							<AccordionPanel pb={4} overflowY='scroll' maxH='70vh' >
								<RadioButtons name='tagOperation' changeFunc={handleToggle} />
								<VStack align={'left'}>
									{tags.map((tag) => {
										return (
											<Checkbox onChange={(e) => handleCheckBoxChange('tags', tag.id, e.target.checked)}>{tag.name}</Checkbox>
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

							<AccordionPanel pb={4} overflowY='scroll' maxH='70vh' >
								<RadioButtons name='projectOperation' changeFunc={handleToggle} />
								<VStack align={'left'}>

									{projects.map((project) => {
										return (
											<Checkbox sx={{ color: '#000' }} style={{ color: '#000' }} onChange={(e) => handleCheckBoxChange('projects', project.id, e.target.checked)}> {project.projectName}</Checkbox>
										);
									})}
								</VStack>
							</AccordionPanel>
						</AccordionItem>
					</AccordionPanel>
				</AccordionItem>
			</Accordion>
			<RadioButtons name='attributeOperation' changeFunc={handleToggle} />

			{searchData['attributes'].map((input, index) => {
				console.log(input);
				return (
					<HStack key={index} marginY={5} paddingY={5} display={'flex'} flexDirection='column' width={'90%'} gap={4} overflowY='scroll'>
						<Select name='attributeID' value={input.attributeID} onChange={event => handleFormChange(index, event)} border={'1px solid'} width={'80%'}>
							{attributes.map((attribute, index) => {
								return <option value={attribute.attributeID}>{attribute.attributeName}</option>;
							})}

						</Select>
						<Select name='operation' value={input.operation} onChange={event => handleFormChange(index, event)} border={'1px solid'} width={'80%'}>
							<option value='EQUALS'>=</option>
							<option value='LIKE'>LIKE</option>
							<option value='HAS'>HAS</option>
						</Select>
						{input.operation !== 'HAS' &&
							<Input
								width={'80%'}
								name='attributeValue'
								placeholder='Attribute value'
								value={input.attributeValue}
								onChange={event => handleFormChange(index, event)}
								color='#000'
								fontsize={'16'}
								bgColor={'white'}
								border={'1px solid'}
							/>}
						<Button onClick={() => removeFields(index)} paddingY={5} paddingx={20} width={'80%'}>Remove</Button>
					</HStack>
				);
			})}
			<HStack display={'flex'} justifyContent='space-between'>
				<Button onClick={addFields}>Add More</Button>
				<Button onClick={filter}>Filter</Button>
			</HStack>
		</Box>
	);
};
export default AssetSearcher;
