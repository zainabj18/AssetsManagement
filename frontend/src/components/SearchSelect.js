import {Box, IconButton, Input,Text,Menu,MenuButton,MenuItemOption,MenuList,Popover,PopoverContent,PopoverTrigger, Portal, UnorderedList, PopoverFooter, ButtonGroup, PopoverHeader, PopoverArrow, PopoverCloseButton, PopoverBody,useDisclosure, useBoolean, HStack, Icon, PopoverAnchor} from '@chakra-ui/react';
import { useEffect,useRef,useState } from 'react';
import {EditIcon,CheckIcon} from '@chakra-ui/icons';
import tags from '../mock_tags.json';
const SearchSelect = () => {
	const [data, setData] = useState([]);
	const [results, setResults] = useState([]);
	const [isEditing, setIsEditing] = useBoolean();

	

	const getData=()=>{
		setData(tags.data);
		setResults(tags.data.slice(0,5));
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
				isLazy
				lazyBehavior='keepMounted'
			>
				<HStack>
					<PopoverAnchor>
						<Input type={'text'}/>
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
                    >{d.name}</Box>);})
						}
					</PopoverBody>
				</PopoverContent>
			</Popover>

		</> );
};
 
export default SearchSelect;