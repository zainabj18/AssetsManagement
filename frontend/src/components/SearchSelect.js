import {Box, IconButton, Input,Text,Menu,MenuButton,MenuItemOption,MenuList,Popover,PopoverContent,PopoverTrigger, Portal, UnorderedList, PopoverFooter, ButtonGroup, PopoverHeader, PopoverArrow, PopoverCloseButton, PopoverBody,useDisclosure, useBoolean, HStack, Icon, PopoverAnchor} from '@chakra-ui/react';
import { useEffect,useRef,useState } from 'react';
import {EditIcon,CheckIcon} from '@chakra-ui/icons';
import tags from '../mock_tags.json';
const SearchSelect = () => {
	const [data, setData] = useState([]);
	const [results, setResults] = useState([]);
	const [isEditing, setIsEditing] = useBoolean();
	const [selectedValue,setSelectedValue]=useState();
	const [searchQuery, setSearchQuery] = useState('');

	

	const getData=()=>{
		setData(tags.data);
		setResults(tags.data.slice(0,5));
	};

	const handleClick=(d)=>{
		setSelectedValue(d);
		setIsEditing.off();
	};

	useEffect(() => {
		getData();
	}, []);
    
	return ( 
		<>
			<Popover
				placement='bottom'
				isOpen={isEditing}
				onOpen={setIsEditing.on}
				onClose={setIsEditing.off}
				closeOnBlur={false}
				closeOnEsc={false}
			>
				<HStack>
					<PopoverAnchor>
						<Input type='text' isReadOnly={!isEditing} onInput={e => setSearchQuery(e.target.value)}/>
					</PopoverAnchor>
					<PopoverTrigger>
						<IconButton size='sm' icon={isEditing ? <CheckIcon /> : <EditIcon />} />
					</PopoverTrigger>
				</HStack>
				
				<PopoverContent>
					<PopoverBody>
						{results.length>0 &&
                    results.map((d)=>{return (<Box
                    	_hover={{ fontWeight: 'semibold',background: 'white',
                    		color: 'teal.500', }}
                    	key={d.id}
                    	onClick={e=>{
                    		handleClick(d);
                    	}}
                    >{d.name}</Box>);})
						}
					</PopoverBody>
				</PopoverContent>
			</Popover>

		</> );
};
 
export default SearchSelect;