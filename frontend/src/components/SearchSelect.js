import {Box, IconButton, Input,Text,Menu,MenuButton,MenuItemOption,MenuList,Popover,PopoverContent,PopoverTrigger, Portal, UnorderedList, PopoverFooter, ButtonGroup, PopoverHeader, PopoverArrow, PopoverCloseButton, PopoverBody,useDisclosure, useBoolean, HStack, Icon, PopoverAnchor} from '@chakra-ui/react';
import { useEffect,useRef,useState } from 'react';
import {EditIcon, CloseIcon} from '@chakra-ui/icons';
import tags from '../MOCK_DATA.json';
const SearchSelect = () => {
	const [data, setData] = useState([]);
	const [results, setResults] = useState([]);
	const [isEditing, setIsEditing] = useBoolean();
	const [selectedValue,setSelectedValue]=useState();
	const [maxVisible,setMaxVisible] = useState(15);
	const [searchQuery, setSearchQuery] = useState('');

	

	const getData=()=>{
		setData(tags.data);
		setResults(tags.data);
	};
	const handleScroll = (e) => {
		const bottom = e.target.scrollHeight-e.target.clientHeight-e.target.scrollTop <5;
		console.log('scorlling');
		if (bottom && maxVisible<results.length) { 
			setMaxVisible(maxVisible+10);
			console.log('I need more data'); }
	};
	const handleClick=(d)=>{
		setSelectedValue(d);
		setIsEditing.off();
		setMaxVisible(15);
	};

	const handleQuery=(query)=>{
		setSearchQuery(query);
		if (query.length > 0) {
            
			setResults(
				data.filter((d) => {
					return d.name.toLowerCase().includes(query.toLowerCase());
				}));
		}};

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
						<Input type='text' isReadOnly={!isEditing} value={searchQuery} placeholder={(selectedValue&&selectedValue.name)||''} onChange={e => {
							handleQuery(e.target.value);}}/>
					</PopoverAnchor>
					<PopoverTrigger>
						<IconButton size='sm' icon={isEditing ? <CloseIcon /> : <EditIcon />} onClick={()=>{
							if (isEditing){
								setSearchQuery('');
							}
						}}/>
					</PopoverTrigger>
				</HStack>
				
				<PopoverContent>
					<PopoverBody overflowY={'scroll'} maxHeight={'xs'} onScroll={handleScroll}>
						{selectedValue && <Box fontWeight='bold' color='teal.600' background='grey'
                    	key={selectedValue.id}
                    	onClick={e=>{
                    		handleClick(selectedValue);
                    	}}
						>{selectedValue.name} (Selected)</Box>}
						{results.length>0 &&
                    results.slice(0,maxVisible).map((d)=>{return (<Box
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