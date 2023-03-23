import { Box, Container, List, ListIcon, ListItem, UnorderedList } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Link, NavLink, useParams } from 'react-router-dom';
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
	return (<Container overflowY='scroll' maxH="70vh"><Accordion allowMultiple>
		{logs && logs.map((log,index)=>{return <AccordionItem key={index}>
			<AccordionButton>
				<Box as="span" flex='1' textAlign='left'>
					{new Date(log.date).toLocaleString()}
				</Box>
				<AccordionIcon />
			</AccordionButton>
			<AccordionPanel pb={2}>
				<List spacing={3}  pb={2}>
					
					{log.diff.added && log.diff.added.length>0 && <ListItem>
						<ListIcon as={AddIcon} color='green.500' />
						<UnorderedList spacing={3}>
							{log.diff.added && log.diff.added.map((add,index)=>{
								return <ListItem key={index}>{add}</ListItem>;
							})} 
						</UnorderedList>
					</ListItem>}
					{log.diff.changed && log.diff.changed.length>0 && <ListItem>
						<ListIcon as={EditIcon} color='orange.500' />
						<UnorderedList spacing={3}>
							{log.diff.changed && log.diff.changed.map((change,index)=>{
								return <ListItem key={index}>{change[0]} from {JSON.stringify(change[1])} to  {JSON.stringify(change[2])} </ListItem>;
							})} 
						</UnorderedList>
					</ListItem>}
					{log.diff.removed && log.diff.removed.length>0 && <ListItem>
						<ListIcon as={CloseIcon} color='red.500' />
						<UnorderedList spacing={3}>
							{log.diff.removed && log.diff.removed.map((remove,index)=>{
								return <ListItem key={index}>{remove}</ListItem>;
							})} 
						</UnorderedList>
					</ListItem>}
					
				</List>
				<Box>
					<Link to={`/profile/${log.accountID}`} as={NavLink}><Text as='i'>Prefromed by {log.username}</Text></Link></Box>
			</AccordionPanel>
		</AccordionItem>;})}
	</Accordion></Container>);
};
 
export default AssetLogs;