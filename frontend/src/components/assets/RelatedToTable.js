import { Container, Heading } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import AssetTable from './AssetTable';
const RelatedType = ({relatedFunc}) => {
	const location = useLocation();
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const [name, setName] = useState('');
	const [cols, setCols] = useState({});

	useEffect(() => {
		console.log(location);
		let name = location.pathname.slice(location.pathname.lastIndexOf('/')+1 , location.pathname.length);
		setName(name);
		relatedFunc(id).then((data)=>{ console.log(data.data);
			if(data.data[0].hasOwnProperty('count')){
				setCols({'count':{
					header: name+' in Common',
					canFilter:true,
				}});
			}else{
				setCols({});
			}
			setAssets(data.data);});
	}, [relatedFunc])
	;
	return (<Container p={4} maxW='100%'>
		<Heading style={{textTransform:'capitalize'}}>Assets Related by {name}</Heading>
		<AssetTable assets={assetsin} setSelectedAssets={null} preSelIDs={[]} cols={cols}/>
	</Container>
	);
};
 
export default RelatedType;