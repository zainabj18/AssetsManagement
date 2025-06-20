import {Box, IconButton, Input,Popover,PopoverContent,PopoverTrigger,PopoverAnchor,HStack,PopoverBody, useBoolean} from '@chakra-ui/react';
import { useEffect,useState } from 'react';
import {EditIcon, CloseIcon} from '@chakra-ui/icons';
const SearchSelect = ({dataFunc,selectedValue,setSelectedValue,createFunc}) => {
	const defaultVisible=15;
	const [results, setResults] = useState([]);
	const [data, setData] = useState([]);
	const [isEditing, setIsEditing] = useBoolean();
	const [maxVisible,setMaxVisible] = useState(defaultVisible);
	const [searchQuery, setSearchQuery] = useState('');
	const [canCreate, setCanCreate] = useBoolean();
	const handleScroll = (e) => {
		const bottom = e.target.scrollHeight-e.target.clientHeight-e.target.scrollTop <5;
		console.log('scorlling');
		if (bottom && maxVisible<results.length) { 
			setMaxVisible((v) => v +10);
		}
	};

	const reset=()=>{
		setSearchQuery('');
		setIsEditing.off();
		setCanCreate.off();
		setMaxVisible(defaultVisible);
		setResults(data);
	};
	const handleClick=(d)=>{
		setSelectedValue(d);
		reset();
	};
	

	const handleCreate=async()=>{
		console.log('creating'+searchQuery);
		await createFunc(searchQuery).then((d) => { 
			console.log(d.data);
			setSelectedValue(d.data); });
		reset();
		getNewData();
	};

	const handleQuery=(query)=>{
		

		setSearchQuery(query);
		if (data.length<1 && query.length > 0){
			setCanCreate.on();
		}else{
			if (query.length > 0){
				let filteredResults=data.filter((d) => {
					return d.name.toLowerCase().includes(query.toLowerCase());
				});
				setResults(filteredResults);
				console.log('I am fileted results',filteredResults);
				if (filteredResults.length===0){
					setCanCreate.on();
				}else{
					setCanCreate.off();
				}
			}else{
				setCanCreate.off();
				setResults(data);
			}
		}
	};
	const getNewData=()=>{
		dataFunc().then(res=>{
			setData(res.data);
			setResults(res.data);
		});
		
	};
	useEffect(() => {
		console.log(dataFunc);
		getNewData();
		
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
				isLazy
			>
				<HStack>
					
					<PopoverAnchor>
						{isEditing ?(<Input type='text' color='red'  value={searchQuery} onChange={e => {
							handleQuery(e.target.value);}}/>):(<Box>{selectedValue&&selectedValue.name}</Box>)}
					</PopoverAnchor>
					<PopoverTrigger>
						<IconButton size='sm' icon={isEditing ? <CloseIcon /> : <EditIcon />} onClick={()=>{
							if (isEditing){
								reset();
							}
						}}/>
					</PopoverTrigger>
				</HStack>
				
				<PopoverContent color={'black'} border={1}>
					<PopoverBody overflowY={'scroll'} maxHeight={'xs'} onScroll={handleScroll}>
						{selectedValue && <Box fontWeight='bold' color='#ed7966's
                    	key={selectedValue.id}
                    	onClick={e=>{
                    		handleClick(selectedValue);
                    	}}
						>{selectedValue.name} (Selected)</Box>}
						{results.length>0 &&
                    results.slice(0,maxVisible).map((d)=>{return (<Box
                    	_hover={{ fontWeight: 'semibold',background: 'white',
                    		color: '#ed796', }}
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