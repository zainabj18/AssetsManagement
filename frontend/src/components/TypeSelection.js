import {
	Checkbox,
	FormControl, FormLabel,
} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { fetchTypesList } from '../api';
import TypeMethodManager from './TypeMethodManager';

const TypeSelection = ({ selectedTypes_state, set_selectedTypes_state, excludeIds = [] }) => {

	const [allTypes, set_allTypes] = useState([]);

	useEffect(() => {
		async function load_allTypes() {
			let data = (await fetchTypesList(res => res.data)).data;
			let modifiedData = TypeMethodManager.removeTheseFromList(data, excludeIds);
			set_allTypes(modifiedData);
		}
		load_allTypes();
	}, [excludeIds]);

	const selectType = (id) => {
		let selectedData = [...selectedTypes_state];
		selectedData.push(id);
		set_selectedTypes_state(selectedData);
	};

	const deselectType = (item) => {
		let selectedData = [...selectedTypes_state];
		let index = selectedData.indexOf(item);
		selectedData.splice(index, 1);
		set_selectedTypes_state(selectedData);
	};

	const ajustSelectedTypes = (checked, id) => {
		if (checked) {
			selectType(id);
		}
		if (!checked) {
			deselectType(id);
		}
	};

	const checkChecked = (id) => {
		if (typeof selectedTypes_state !== 'undefined') {
			return [...selectedTypes_state].includes(id);
		}
		else {
			return false;
		}
	};

	return (
		<FormControl>
			<FormLabel>Depends On</FormLabel>
			{allTypes.map((type) => {
				return (
					<Checkbox
						key={type.type_id}
						isChecked={checkChecked(type.type_id)}
						onChange={(e) => {
							ajustSelectedTypes(e.target.checked, type.type_id);
						}}
					>
						{type.type_name}
					</Checkbox>
				);
			})}
		</FormControl>
	);
};

export default TypeSelection;