import { Box, Container, List, ListIcon, ListItem, UnorderedList } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAssetsLogs } from '../../api';
import {
	Accordion,
	AccordionItem,
	AccordionButton,
	AccordionPanel,
	AccordionIcon,
	Text,
} from '@chakra-ui/react';
import { CloseIcon, AddIcon, EditIcon } from '@chakra-ui/icons';
const AssetLogs = () => {
	const { id } = useParams();
	const [logs, setLogs] = useState([]);

	useEffect(() => {
		fetchAssetsLogs(id).then((data)=>{ console.log(data.data);
			setLogs(data.data);});
	}, [])
	;
	return (<Container><Accordion allowMultiple>
		{logs && logs.map((log,index)=>{return <AccordionItem key={index}>
			<AccordionButton>
				<Box as="span" flex='1' textAlign='left'>
					{log.date}
				</Box>
				<AccordionIcon />
			</AccordionButton>
			<AccordionPanel pb={2}>
				<List spacing={3}  pb={2}>
					<ListItem>
						<ListIcon as={AddIcon} color='green.500' />
						<UnorderedList spacing={3}>
							{log.diff.added && log.diff.added.map((add,index)=>{
								return <ListItem key={index}>{add}</ListItem>;
							})} 
						</UnorderedList>
						{log.diff.added.length===0 && <Box>No adds</Box>}
					</ListItem>
					<ListItem>
						<ListIcon as={EditIcon} color='orange.500' />
						<UnorderedList spacing={3}>
							{log.diff.changed && log.diff.changed.map((change,index)=>{
								return <ListItem key={index}>{change[0]} from {JSON.stringify(change[1])} to  {JSON.stringify(change[2])} </ListItem>;
							})} 
						</UnorderedList>
						{log.diff.changed.length===0 && <Box>No change</Box>}
					</ListItem>
					<ListItem>
						<ListIcon as={CloseIcon} color='red.500' />
						<UnorderedList spacing={3}>
							{log.diff.removed && log.diff.removed.map((remove,index)=>{
								return <ListItem key={index}>{remove}</ListItem>;
							})} 
						</UnorderedList>
						{log.diff.removed.length===0 && <Box>No removes</Box>}
					</ListItem>
				</List>
				<Box><Text as='i'>Prefromed by {log.username}</Text></Box>
			</AccordionPanel>
		</AccordionItem>;})}
	</Accordion></Container>);
};
 
export default AssetLogs;