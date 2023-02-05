import {Box, IconButton, Input,Popover,PopoverContent,PopoverTrigger,PopoverAnchor,HStack,PopoverBody, useBoolean} from '@chakra-ui/react';
import { useEffect,useState,useMemo } from 'react';
import {EditIcon, CloseIcon} from '@chakra-ui/icons';
const SearchSelect = ({dataFunc,selectedValue,setSelectedValue,createFunc}) => {
	const defaultVisible=15;
	const [results, setResults] = useState([]);
	const [isEditing, setIsEditing] = useBoolean();
	const [maxVisible,setMaxVisible] = useState(defaultVisible);
	const [searchQuery, setSearchQuery] = useState('');
	const [canCreate, setCanCreate] = useBoolean();
	const [isDisabled, setIsDisabled] = useBoolean(false);
	const [newData, setNewData] = useBoolean();
	const data = useMemo(() => dataFunc(), [newData]);

	const handleScroll = (e) => {
		const bottom = e.target.scrollHeight-e.target.clientHeight-e.target.scrollTop <5;
		console.log('scorlling');
		if (bottom && maxVisible<results.length) { 
			setMaxVisible((v) => v +10);
		}
	};

	const reset=()=>{
		setIsEditing.off();
		setCanCreate.off();
		setMaxVisible(defaultVisible);
		setSearchQuery('');
		setResults(data);
	};
	const handleClick=(d)=>{
		setSelectedValue(d);
		reset();
	};

	const handleCreate=()=>{
		console.log('creating'+searchQuery);
		setIsDisabled.on();
		createFunc(searchQuery).then((d) => { setSelectedValue(d); });
		setIsDisabled.off();
		setNewData.toggle();
		reset();
	};

	const handleQuery=(query)=>{
		setSearchQuery(query);
		if (query.length > 0) {
			let filteredResults=data.filter((d) => {
				return d.name.toLowerCase().includes(query.toLowerCase());
			});
			setResults(filteredResults);
			if (filteredResults.length===0){
				setCanCreate.on();
			}	
		}};

	useEffect(() => {
		setResults(data);
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
						<Input type='text' isDisabled={isDisabled} isReadOnly={!isEditing} value={searchQuery} placeholder={(selectedValue&&selectedValue.name)||''} onChange={e => {
							handleQuery(e.target.value);}}/>
					</PopoverAnchor>
					<PopoverTrigger>
						<IconButton size='sm' icon={isEditing ? <CloseIcon /> : <EditIcon />} onClick={()=>{
							if (isEditing){
								reset();
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
						{canCreate && <Box _hover={{ fontWeight: 'semibold',background: 'white',
                    		color: 'teal.500', }} onClick={handleCreate}>Create new {searchQuery}</Box>}
					</PopoverBody>
				</PopoverContent>
			</Popover>

		</> );
};
 
export default SearchSelect;