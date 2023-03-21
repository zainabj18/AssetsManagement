import { Input } from '@chakra-ui/react';
import React, { useState } from 'react';
import { useAsyncDebounce } from 'react-table';
const GlobalFilter = ({globalFilter,setGlobalFilter}) => {
	const [value, setValue] = useState(globalFilter);

	// delays the filtering of the table on input
	const onChange = useAsyncDebounce(value => {
		setGlobalFilter(value || undefined);
	}, 200);
  
	return (
		<>
			<Input value={value || ''} onChange={e => {
				setValue(e.target.value);
				onChange(e.target.value);
			}} placeholder="Search"/>
		</>
	);
};

export default GlobalFilter;