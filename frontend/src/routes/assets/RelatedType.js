import { useEffect, useState } from 'react';
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
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]}/>);
};
 
export default RelatedType;