import { Button, Text, useBoolean } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchType } from '../api';

const TypeEditer = () => {
	let { id } = useParams(); 

	const [toggle, set_toggle] = useBoolean();

	const [type, set_type] = useState([]);

	useEffect(() => {
		async function load_type() {
			let data = await fetchType(id, res => res.data);
			set_type(data);
		}
		load_type();
	}, [toggle]);

	return (
		<>
			<Text>TypeEditer</Text>
			<Button onClick={() => console.log(type)}>Log Type</Button>
		</>
	);
};

export default TypeEditer;