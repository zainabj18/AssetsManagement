import { Input,Popover,PopoverContent,PopoverTrigger } from '@chakra-ui/react';
import { useEffect,useState } from 'react';
import tags from '../mock_tags.json';
const SearchSelect = () => {
	const [data, setData] = useState([]);

	const getData=()=>{
		setData(tags.data);
	};

	useEffect(() => {
		getData();
	}, []);
    
	return ( 
		<>
			<Input type="text"/>
			{data.length>0 && <Popover>
				<PopoverTrigger>
					<Input type="text"/>
				</PopoverTrigger>
				<PopoverContent>
					{data.map((tag)=>{
						return (<div>{tag.name}</div>);
					})}
				</PopoverContent>

			</Popover>

			}

		</> );
};
 
export default SearchSelect;