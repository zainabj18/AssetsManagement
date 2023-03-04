import { Heading, VStack, useBoolean } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchType } from '../api';
import AttributeSelection from '../components/AttributeSelection';

const TypeEditer = () => {
	let { id } = useParams(); 

	const [toggle, set_toggle] = useBoolean();

	const [type, set_type] = useState([]);

	useEffect(() => {
		async function load_type() {
			let data = await fetchType(id, res => res.data);
			set_type(data);
			set_selectedAttributes(data.metadata);
		}
		load_type();
	}, [toggle]);

	const [selectedAttributes, set_selectedAttributes] = useState([]);
	useEffect(() => {
		set_selectedAttributes_hasError(selectedAttributes.length < 1);
	}, [selectedAttributes]);

	const [load_attribute_trigger, set_load_attribute_trigger] = useBoolean();
	const [selectedAttributes_hasError, set_selectedAttributes_hasError] = useState(false);

	return (
		<VStack align='stetch'>
			<Heading as='h1' size='2xl'>Type: {type.typeName}</Heading>
			<Heading as='h2' size='1xl'>Version: {type.versionNumber}</Heading>
			<AttributeSelection
				selectedAttributes_state={selectedAttributes}
				set_selectedAttributes_state={set_selectedAttributes}
				load_attribute_trigger={load_attribute_trigger}
				isInvalid={selectedAttributes_hasError}
			/>
		</VStack>
	);
};

export default TypeEditer;