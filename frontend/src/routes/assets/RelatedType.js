import { useEffect, useState } from 'react';
import { VStack } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';
import {fetchRelatedClassification, fetchRelatedTags, fetchRelatedType } from '../../api';

import AssetTable from '../../components/AssetTable';
const RelatedType = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);

	useEffect(() => {
		fetchRelatedType(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<VStack  width={"80vw"} background="white" paddingX={5} paddingY={5} rounded="2xl"  boxShadow="0 3px 6px #00000029">
        <AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]}/>
    </VStack>);
};
 
export default RelatedType;