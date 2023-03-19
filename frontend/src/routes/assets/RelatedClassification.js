import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedClassification, fetchRelatedTags } from '../../api';

import AssetTable from '../../components/assets/AssetTable';
const RelatedClassification = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);

	useEffect(() => {
		fetchRelatedClassification(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]}/>);
};
 
export default RelatedClassification;