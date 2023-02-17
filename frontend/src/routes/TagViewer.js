import { Badge, Heading,VStack } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAssetsinTag } from '../api';
import CustomTable from '../components/CustomTable';

const TagViewer = () => {
	const [assets, setAssets] = useState([]);
	const [tag, setTag] = useState('');
	const { id } = useParams();

	const columns =useMemo(()=>
	{ return {
		
		
		'asset_id':{
			header: 'Asset ID',
			canFilter:true	
		},
		'name':{
			header: 'Asset Name',
			canFilter:true
		},
		'type':{
			header: 'Asset Type',
			canFilter:true
		},
		'classification':{
			header: 'Asset Classification',
			canFilter:true,
			Cell:(rowID,value)=>{return <Badge>{value}</Badge>;}
		},
	};
	}
	,[]);

	

	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
		console.log(assets);
	}, [id]);
    
	return ( <VStack bg={'whiteAlpha.500'} h={'100%'} w={'100%'} p={2}>
		<Heading>{tag}</Heading>
		<CustomTable rows={assets} cols={columns} setSelectedRows={()=>{}}/>
	</VStack> );
};
 
export default TagViewer;