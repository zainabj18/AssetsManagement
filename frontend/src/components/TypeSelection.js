import {
	Checkbox,
	FormControl, FormLabel,
	useBoolean,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { fetchTypesList } from '../api';

const TypeSelection = ({set_selectedTypes_state}) => {

	const [trigger_load_types] = useBoolean();
	const [allTypes, set_allTypes] = useState([]);
	const [selectedTypes, set_selectedTypes] = useState([]);

	useEffect(() => {
		set_selectedTypes_state(selectedTypes);
	}, [selectedTypes]);

	useEffect(() => {
		async function load_allTypes() {
			let data = (await fetchTypesList(res => res.data)).data;
			set_allTypes(data);
		}
		load_allTypes();
	}, [trigger_load_types]);

	const selectType = (id) => {
		selectedTypes.push(id);
		set_selectedTypes(selectedTypes);
	};

	const deselectType = (item) => {
		let index = selectedTypes.indexOf(item);
		selectedTypes.splice(index, 1);
		set_selectedTypes(selectedTypes);
	};

	const ajustSelectedTypes = (checked, id) => {
		if (checked) {
			selectType(id);
		}
		if (!checked) {
			deselectType(id);
		}
	};
	
	return (
		<FormControl>
			<FormLabel>Depends On</FormLabel>
			{allTypes.map((allTypes) => {
				return (
					<Checkbox
						key={allTypes.type_id}
						onChange={(e) => {
							ajustSelectedTypes(e.target.checked, allTypes.type_id);
						}}
					>
						{allTypes.type_name}
					</Checkbox>
				);
			})}
		</FormControl>
	);
};

export default TypeSelection;