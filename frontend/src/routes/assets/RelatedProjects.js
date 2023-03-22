import { useEffect, useState } from 'react';
import { VStack } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';
import {fetchRelatedProjects, fetchRelatedTags } from '../../api';

import AssetTable from '../../components/AssetTable';
const RelatedProjects = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const link_col={'count':{
		header: 'Projects in Common',
		canFilter:true,
	}};

	useEffect(() => {
		fetchRelatedProjects(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (
		<div>
    <VStack  width={"80vw"} background="white" paddingX={5} paddingY={5} rounded="2xl"  boxShadow="0 3px 6px #00000029">        
	<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]} cols={link_col}/>
    </VStack>
	</div>
	);
};
 
export default RelatedProjects;