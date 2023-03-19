import { Container,Tabs,TabList,TabPanels,Tab} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';

const AssetOverview=() => {
	const navigate = useNavigate();
	const location = useLocation();
	const [defaultIndex, setDefaultIndex] = useState(0);
	const [tabs, setTabs] = useState([{to:'./',name:'Attributes'},
		{to:'./classification',name:'Classification'},
		{to:'./type',name:'Type'},
		{to:'./tags',name:'Tags'},
		{to:'./projects',name:'Projects'},
		{to:'./outgoing',name:'Outgoing Asset Links'},
		{to:'./incomming',name:'Incomming Asset Links'},
		{to:'./comments',name:'Comments'},
		{to:'./logs',name:'Logs'}]);

	useEffect(() => {
		let name = location.pathname.slice(location.pathname.lastIndexOf('/') , location.pathname.length);
		for (var i = 0; i < tabs.length; i++) { 
			
			if(tabs[i].to==='.'+name){
				console.log('here');
				setDefaultIndex(i);
				break;
			}
		}
	}, []);
		
	return ( 
		<Container minW="100%">
			{defaultIndex && <Tabs isFitted variant='enclosed' onChange={(e)=>navigate(tabs[e].to)} bg={'white'} defaultIndex={defaultIndex}>
				<TabList>
					{tabs.map((tab,index)=>{
						return (
							<Tab _selected={{bg: 'blue.100' }} key={index}>{tab.name}</Tab>);
					})}
				</TabList>
				<TabPanels bg="blue.100">
					<Outlet />	
				</TabPanels>
			</Tabs>}
			

		</Container>);
};
 
export default AssetOverview
;