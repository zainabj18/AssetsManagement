import {Box, Button, Input,Text,Menu,MenuButton,MenuItemOption,MenuList,Popover,PopoverContent,PopoverTrigger, Portal, UnorderedList, PopoverFooter, ButtonGroup, PopoverHeader, PopoverArrow, PopoverCloseButton, PopoverBody,useDisclosure} from '@chakra-ui/react';
import { useEffect,useRef,useState } from 'react';
import tags from '../mock_tags.json';
const SearchSelect = () => {
	const [data, setData] = useState([]);
	const [results, setResults] = useState([]);
	const { isOpen, onToggle, onClose } = useDisclosure();

	

	const getData=()=>{
		setData(tags.data);
	};

	useEffect(() => {
		getData();
		setResults(data.slice(0,5));
	}, []);
    
	return ( 
		<>
			
			<Popover
				placement='bottom'
				isOpen={isOpen}
				onClose={onClose}
			>
				<PopoverTrigger>
					<Input mr={5} onClick={onToggle}/>
				</PopoverTrigger>
				<PopoverContent>
					<Text>Hello</Text>
				</PopoverContent>
			</Popover>

		</> );
};
 
export default SearchSelect;